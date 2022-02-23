import sys

from modules.export.adt import export
from modules.export.data import ResultSelector, Selector, Col, EurColPops, NumCol, SensSpecCalc, KeySelector, MultCol
from modules.output.results_import import from_file
from modules.runners.run import RunResult

file = "combotable.txt"

POPS = 10

value_lists = []
while POPS <= 150:
    inputs = from_file(file, POPS*1000)

    a = []
    for input in inputs:
        a.append(input)

    value_lists.append(a)
    POPS += 10


def show_entries(value_lists, col: Col):
    print("A,B,C,D,E,F,G,H")
    for value_list in value_lists:
        r = ""
        for l in value_list:
            entry = col.get_data(l)
            if len(r) == 0:
                r += str(l.keys.get("POPS"))
            r += ","
            r += str(float(entry))

        print(r)


print("-- Total Patients")
show_entries(value_lists, MultCol("Total Patients", KeySelector("POPS"), ResultSelector(7), unit="Persons", rr=False))

print("-- Total Cost")
show_entries(value_lists, EurColPops("Total Cost", ResultSelector(5), rr=False))

