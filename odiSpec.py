import sys

from graphDataCreation import graph_run, show_entries
from modules.export.adt import export
from modules.export.data import ResultSelector, Selector, Col, EurColPops, NumCol, SensSpecCalc, EuroConditionalCalc
from modules.output.results_import import from_file
from modules.runners.run import RunResult

file = "odiSpecExp.txt"

POPS = 70000
value_lists = graph_run(file, POPS, "int FP", 1, 0)


print("-- Time to Diagnosis")
show_entries(value_lists, NumCol("Time to Diagnosis", ResultSelector(6), unit="Days"), "int FP")

print("-- Cost")
show_entries(value_lists, EurColPops("Total Cost", ResultSelector(5), rr=False), "int FP")

print("-- Cost per Treatment")
show_entries(value_lists, EuroConditionalCalc("Cost per Treatment", ResultSelector(5), ResultSelector(7), rr=False) , "int FP")

print("-- Sens")
show_entries(value_lists, SensSpecCalc("Sensitivity", ResultSelector(1), ResultSelector(0)), "int FP")


print("-- Spec")
show_entries(value_lists, SensSpecCalc("Specificity",ResultSelector(3), ResultSelector(0), neg=True), "int FP")