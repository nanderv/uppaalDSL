from modules.export.data import Col
from modules.output.results_import import from_file


def graph_run(file, POPS, combine_str, mult=100, result_id=1):
    inputs = from_file(file, POPS)

    bins = dict()
    for input in inputs:
        kz = bins.get(input.keys.get("GP"), [])
        kz.append(input)
        bins[input.keys.get("GP")] = kz

    def sorter(input):
        return float(input.keys.get(combine_str))

    for z in bins:
        bins[z].sort(key=sorter)

    value_lists = []
    while True:
        skipped = False
        res = []
        for z in bins:

            if len(bins[z]) == 0:
                skipped = True
                continue
            a = bins[z].pop(0)
            res.append(a)
        value_lists.append(res)
        if skipped:
            break

    return value_lists


def show_entries(value_lists, col: Col, combine_str, mult=1):
    print("A,B,C,D,E,F,G,H")
    for value_list in value_lists:
        r = ""
        for l in value_list:
            entry = col.get_data(l)
            if len(r) == 0:
                r += l.keys.get(combine_str)
            r += ","
            r += str(float(entry)*mult)
        print(r)
