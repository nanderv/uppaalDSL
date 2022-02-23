import itertools
from copy import deepcopy

from lark import Lark, Tree

from modules.transformations.transform import BaseTransformation

test_grammar = r"""
    ?start: scope
    
    ?statement: scope -> scope
                | COMMENT
               | "import(" [string] ")" -> import
              | "merge(" [string] ")" -> merge

               | "addTemplateChoices(" [string] ")"          -> add_template_choices    
               | "addTemplateChoice(" [string "," value "," string] ")" -> add_template_choice
               | "setLocalValue(" [string "," string "," value] ")" -> set_template_value
              | "setGlobalValue(" [string "," value] ")" -> set_global_value

               | "setLocalIntSweep(" [string "," string "," SIGNED_NUMBER "," SIGNED_NUMBER "," SIGNED_NUMBER] ")" -> local_int_sweep
               | "setGlobalIntSweep(" [string "," SIGNED_NUMBER "," SIGNED_NUMBER "," SIGNED_NUMBER] ")" -> global_int_sweep
               | "setLocalIntChoices(" [string "," string ] ")" -> local_int_choices
               | "setGlobalIntChoices(" [string ] ")" -> global_int_choices
               | "setLocalIntChoice(" [string "," string "," SIGNED_NUMBER] ")" -> local_int_choice
               | "setGlobalIntChoice(" [string "," SIGNED_NUMBER] ")" -> global_int_choice
               
               | "setTemplate(" [string "," string "," string] ")" -> set_template

COMMENT: "#" /(.)+/
    scope : "{" statement* "}"
    ?value: string
          | SIGNED_NUMBER      -> number
          | "true"             -> true
          | "false"            -> false
          | "null"             -> null

    ?string : ESCAPED_STRING  

    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore COMMENT
    %ignore WS
"""

syn_parser = Lark(test_grammar, parser='lalr', lexer='basic', propagate_positions=False, maybe_placeholders=False)
parse = syn_parser.parse


class Run(BaseTransformation):
    def __init__(self, param, should_run_phase="declaration", on_template=None):
        self.param = param
        self.should_run_phase = should_run_phase
        self.on_template = on_template
        self.isrun = False

    def get_scope_key(self):
        return "RUN@" + self.param

    def get_value(self):
        return None

    def __str__(self):
        return self.get_scope_key() + " := " + str(self.get_value())

    def unpack(self):
        return [self]

    def should_transform_line(self, line):
        if self.param in line and ("//TRANS" in line.upper() or "//INJECTED" in line.upper()):
            self.isrun=True
            return True
        return False

class SetTemplate(Run):
    def __init__(self, param, value, value_name):
        super(SetTemplate, self).__init__(param, should_run_phase="system")
        self.value = value
        self.value_name = value_name


    def get_value(self):
        return self.value

    def get_value_name(self):
        return self.value_name

    def should_transform_line(self, line):

        if line.strip().startswith(self.param) and ("//TRANS" in line.upper() or "//INJECTED" in line.upper()):
            self.isrun=True
            return True
        return False

    def transformed_line(self, line):
        return self.param + " = " + str(self.value) + "; //injected"


class SetIntValue(Run):
    def __init__(self, param, value, on_template=None):
        if on_template is None:
            super(SetIntValue, self).__init__(param)
        else:
            super(SetIntValue, self).__init__(param, "global", on_template)
        self.value = value

    def get_scope_key(self):
        return "SETINT@" + self.param

    def get_value(self):
        return self.value

    def get_value_name(self):
        return str(self.value)

    def transformed_line(self, line):
        return self.param + " = " + str(self.value) + "; //injected"

class SetReadVal(Run):
    def __init__(self, param, value, on_template=None):
        super().__init__(param, on_template)

    def should_transform_line(self, line):
        self.isrun=True
        return False

class SetIntSweep(SetIntValue):
    def __init__(self, param, mi, ma, step, on_template=None):
        super(SetIntSweep, self).__init__(param, mi, on_template=on_template)
        self.min = int(mi)
        self.max = int(ma)
        self.step = int(step)

    def unpack(self):
        i = self.min
        ret = []
        while i <= self.max:
            ret.append(SetIntValue(self.param, i, on_template=self.on_template))
            i += self.step

        return ret


class SetIntChoice(SetIntValue):
    def __init__(self, param, on_template=None):
        super(SetIntChoice, self).__init__(param, 0, on_template=on_template)
        self.values = []

    def unpack(self):
        return map(lambda x: SetIntValue(self.param, x, on_template=self.on_template), self.values)

    def get_scope_key(self):
        if self.on_template:
            return "SetLocalIntChoice@{} {}".format(self.param, self.on_template)
        return "SetGlobalIntChoice@{}".format(self.param)

    def unpack(self):
        ret = []
        for value in self.values:
            ret.append(SetIntValue(self.param, value, on_template=self.on_template))
        return ret


class SetTemplateChoice(SetTemplate):
    def __init__(self, param):
        super(SetTemplate, self).__init__(param, should_run_phase="system")
        self.value = None
        self.value_name = None
        self.started = False
        self.values = []
        self.values_names = []
        self.pointer = 0

    def get_scope_key(self):
        return "SetTemplateChoice@" + self.param

    def unpack(self):
        i = 0
        ret = []
        while i < len(self.values):
            ret.append(SetTemplate(self.param, self.values[i], self.values_names[i]))
            i += 1
        return ret


def pstr(obj):
    return obj.value.replace('"', "")


def run_scope(sub_tree, scope={}, edge_imports=[]):
    result_scopes = []
    new_scope = deepcopy(scope)
    edge_imports = deepcopy(edge_imports)
    sub_scopes = []
    for inst in sub_tree.children:
        if inst.data == "set_template":
            templ = SetTemplate(pstr(inst.children[0]), pstr(inst.children[1]), pstr(inst.children[2]))
            new_scope[templ.get_scope_key()] = templ

        if inst.data == "set_template_value":
            a = pstr(inst.children[1])
            b = pstr(inst.children[0])
            templ = SetIntValue(a, inst.children[2].children[0].value, b)
            new_scope[templ.get_scope_key()] = templ

        if inst.data == "set_global_value":
            a = pstr(inst.children[0])
            templ = SetIntValue(a, inst.children[1].children[0].value)
            new_scope[templ.get_scope_key()] = templ

        if inst.data == "add_template_choices":
            a = pstr(inst.children[0])
            templ = SetTemplateChoice(a)
            new_scope[templ.get_scope_key()] = templ

        if inst.data == "global_int_sweep":
            a = pstr(inst.children[0])
            templ = SetIntSweep(a, inst.children[1].value, inst.children[2].value,
                                inst.children[3].value)
            new_scope[templ.get_scope_key()] = templ

        if inst.data == "local_int_sweep":
            a = pstr(inst.children[1])
            b = pstr(inst.children[0])

            templ = SetIntSweep(a, inst.children[2].value, inst.children[3].value,
                                inst.children[4].value, b)
            new_scope[templ.get_scope_key()] = templ

        if inst.data == "global_int_choices":
            a = pstr(inst.children[0])
            templ = SetIntChoice(a)
            new_scope[templ.get_scope_key()] = templ

        if inst.data == "local_int_choices":
            a = pstr(inst.children[0])
            templ = SetIntChoice(a, inst.children[1].value)
            new_scope[templ.get_scope_key()] = templ
        if inst.data == "global_int_choice":
            r = new_scope["SetGlobalIntChoice@" + pstr(inst.children[0])]
            r.values.append(pstr(inst.children[1]))
        if inst.data == "local_int_choice":
            r = new_scope['SetLocalIntChoice@{} "{}"'.format( pstr(inst.children[0]), pstr(inst.children[1]))]
            r.values.append(pstr(inst.children[2]))
        if inst.data == "add_template_choice":
            r = new_scope["SetTemplateChoice@" + pstr(inst.children[0])]
            r.values.append(pstr(inst.children[1]))
            r.values_names.append(pstr(inst.children[2]))

        if inst.data == "scope":
            sub_scopes.append(inst)
        if inst.data == "import":
            from modules.transformations.parseparams import parse_file
            with  open("simulations/" + pstr(inst.children[0]), "r") as my_file:
                lines = ""
                while l := my_file.readline():
                    lines += l + "\n"
                    # print(l.strip())
                p = parse(lines)

                sub_scopes.append(p)
        if inst.data == "merge":
            from modules.transformations.parseparams import parse_file
            with  open("simulations/" + pstr(inst.children[0]), "r") as my_file:
                lines = ""
                while l := my_file.readline():
                    lines += l + "\n"
                    # print(l.strip())
                p = parse(lines)

                edge_imports.append(p)

    if len(sub_scopes) == 0:
        if len(edge_imports) == 0:
            result_scopes.append(list(new_scope.values()))
        else:
            sub_scopes.append(edge_imports.pop())


    for scope in sub_scopes:
        result_scopes += run_scope(scope, new_scope, edge_imports)
    return result_scopes


def parse_result_unmapping(prrr):
    result = []
    for z in prrr:
        y = list(map(lambda it: it.unpack(), z))
        c = (itertools.product(*y))
        result += c
    return result
