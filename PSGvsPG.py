import sys

from graphDataCreation import graph_run, show_entries
from modules.export.adt import export
from modules.export.data import ResultSelector, Selector, Col, EurColPops, NumCol, SensSpecCalc
from modules.output.results_import import from_file
from modules.runners.run import RunResult

file = "PSGvsPG.txt"

POPS = 70000


value_lists = graph_run(file, POPS, "int PSGodds", 1, 0)




print("-- Time to Diagnosis")
show_entries(value_lists, NumCol("Time to Diagnosis", ResultSelector(6), unit="Days"), "int PSGodds")

print("-- Cost")
show_entries(value_lists, EurColPops("Total Cost", ResultSelector(5), rr=False), "int PSGodds")

