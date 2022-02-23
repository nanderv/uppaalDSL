import xml.etree.ElementTree


class BaseTransformation:
    """
        Base class of transformation
    """

    def __init__(self):
        self.should_run_phase = ''
        self.isrun = False

    def should_transform_line(self, line):
        pass

    def transformed_line(self, line):
        pass


class TransformSetVariable(BaseTransformation):
    """
        Alter a single variable declaration
        @param variable_decl which variable declaration to change. eg: int OSA_PREV
        @param value which value to substitute it for?
        @param should_run_phase: in which phase to run it
    """

    def __init__(self, variable_decl, value, should_run_phase):
        super().__init__()
        self.variable_decl = variable_decl
        self.value = value
        self.should_run_phase = should_run_phase

    def should_transform_line(self, line):
        if self.variable_decl in line and ("//TRANS" in line.upper() or "//INJECTED" in line.upper()):
            self.isrun = True
            return True

        return False

    def transformed_line(self, line):
        return self.variable_decl + " = " + str(self.value) + "; //injected"


def handle_for_subthing(xml_elem, node_name, transformations: list[BaseTransformation], should_run_name=None):
    if not should_run_name:
        should_run_name = node_name
    """
        handle transformation for one sub_node.
    """
    lc = 0

    lz = xml_elem.find(node_name)
    if lz is None:
        return
    ls = lz.text.splitlines(keepends=False)

    for line in ls:
        for transformation in transformations:
            if transformation.should_run_phase == should_run_name and transformation.should_transform_line(line):
                ls[lc] = transformation.transformed_line(line)
        lc += 1
    xml_elem.find(node_name).text = "\r\n".join(ls)


def handle_for_all_templates(xml_elem, transformations: list[BaseTransformation]):
    for template in xml_elem.findall('template'):
        name = template.find("name").text
        trans = []
        for tra in transformations:
            if tra.should_run_phase == "global" and tra.on_template == name:
                trans.append(tra)
        handle_for_subthing(template, "declaration", trans, should_run_name="global")


def transform_UPPAAL(tree, transformations: list[BaseTransformation]):
    """
        Transformation main function
    """
    handle_for_subthing(tree, 'declaration', transformations)
    handle_for_subthing(tree, 'system', transformations)
    handle_for_all_templates(tree, transformations)
    for transformation in transformations:
        if not transformation.isrun:
            print("ERROR", transformation)
    return tree
