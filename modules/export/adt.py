from modules.export.data import Col, SensSpecCalc, ResultSelector, KeySelector, PercentageCol, EurCol, EuroConditionalCalc, EurColPops, MultCol, NumCol, ConditionalCalc
from modules.export.latexgen import RowGenerator

gen = RowGenerator(
    [
        Col("POPS", KeySelector("POPS")),
        Col("Incidence", KeySelector("INCIDENCE"), unit="\%", line_after=True),
        Col("Scenario", KeySelector("QTEM")),
        SensSpecCalc("Sensitivity", ResultSelector(1), ResultSelector(0)),
        SensSpecCalc("Specificity", ResultSelector(3), ResultSelector(0), neg=True),
        PercentageCol("CPAP Forever", ResultSelector(7)),
        PercentageCol("Percentage other treatment", ResultSelector(10)),
        NumCol("Time to Diagnosis", ResultSelector(6), unit="Days"),
        ConditionalCalc("Time to Cpap Forever", ResultSelector(9), ResultSelector(8), unit="Days", line_after=True),
        EurCol("Cost", ResultSelector(5), ),
        EuroConditionalCalc("Cost per Treatment", ResultSelector(5), ResultSelector(7)),
        EurColPops("Total Cost", ResultSelector(5)),
        MultCol("Total Patients", KeySelector("POPS"), ResultSelector(7), unit="Persons"),
    ]
)




def export(data):
    print(gen.gen(data))

