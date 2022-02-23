from modules.transformations.parse import parse, run_scope, parse_result_unmapping

dd = dict()

def get_pv(key):
    return dd.get(key, key)


def set_pv(key, value):
    dd[key] = value


def parse_file(c, as_import = False):
    file = 'simulations/' + c + "/profile.scn"
    if as_import:
        file = "simulations/"+c
    with  open(file, "r") as my_file:
        lines = ""
        while l := my_file.readline():
            lines += l + "\n"
            # print(l.strip())
        p = parse(lines)

        r = run_scope(p)
        a = parse_result_unmapping(r)
        # print(len(a))
        return a


def addTo(input, add):
    res = []
    for i in input:
        res.append(i)
    res.append(add)
    return res


