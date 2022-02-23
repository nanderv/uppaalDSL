import sys

from modules.export.adt import export
from modules.output.results_import import from_file
from modules.runners.run import RunResult

file = "basic/1.txt"
FUN = "cost"
files = []
POPS = 70000
if len(sys.argv) > 1:
    FUN = sys.argv[1]
if len(sys.argv) > 2:
    POPS = sys.argv[2]
if len(sys.argv) > 3:
    file = sys.argv[3]
i = 4
while len(sys.argv) > i:
    files.append(sys.argv[i])
    i += 1

inputs = []

while file is not None:
    inputs += from_file(file, POPS)

    if len(files) == 0:
        break
    file = files.pop(0)

if FUN == "cost":
    from modules.gfx.costs import cost_table
    print(cost_table(inputs))

if FUN == "costper":
    from modules.gfx.costs import cost_table
    print(cost_table(inputs, per=True))

if FUN =="per":
    from modules.gfx.treatment_percentage import percentage_treatment
    print("THIS ONE WILL BREAK NOW")
    print(percentage_treatment(inputs))

if FUN == "fast":
    export(inputs)

if FUN == "sens":
    from modules.gfx.sensitivity import sensitivity_table
    print(sensitivity_table(inputs))

if FUN == "spec":
    from modules.gfx.specificity import specificity_table
    print(specificity_table(inputs))

if FUN == "npv":
    from modules.gfx.npv import npv_table
    print(npv_table(inputs))

if FUN == "ppv":
    from modules.gfx.ppv import ppv_table
    print(ppv_table(inputs))

if FUN == "wait":
    from modules.gfx.waiting_times import waiting_table
    print(waiting_table(inputs))
"""
P_osa
P_osa&Dosa
P_osa&nDosa
P_nosa&nDosa
P_nosa&Dosa
cost
w_diag
P_w_treatment
w_treatment
P_cdiag
w_cdiag
P_cpdiag
w_cpdiag
p_eotl
w_eotl
p_otreatment
"""
