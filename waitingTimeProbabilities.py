import sys

from graphDataCreation import graph_run, show_entries
from modules.export.data import Col, ResultSelector

file = "maxTime.txt"

POPS = 70000

value_lists = graph_run(file, POPS, "int diagnosisMaximumTime")

show_entries(value_lists, Col("Total Cost", ResultSelector(1)), "int diagnosisMaximumTime", 100)
print("#### Peter table")
show_entries(value_lists, Col("Total Cost", ResultSelector(2)), "int diagnosisMaximumTime", 100)
