def percentage_treatment(results):
    scnz = ""
    for result in results:
        if scnz != "":
            scnz += ","
        scnz += result[0][0].split(",")[1]
    strr = """  \\begin{tikzpicture}
    \\begin{axis}[
    title={Percentage of Patients receiving treatment},
    ybar stacked, ymin=0, ymax=100,
    bar width=10mm,
    symbolic x coords={"""+scnz+"""},
    xtick=data,
    nodes near coords, 
    nodes near coords align={anchor=north},%Move values in bar
    every node near coord/.style={
    },
    ]
    %Active
    \\addplot [fill=cyan] coordinates {\n"""
    for result in results:
        best_result = 0
        for r in result:
            best_result = max(int(float(r[1].split(",")[16])*100), best_result)
        strr += "({"+result[0][0].split(",")[1]+"}, " +str(best_result) + ")\n"

    strr += """
    };
    %Inactive
    \\addplot [fill=red] coordinates {\n"""
    for result in results:
        best_result = 0
        for r in result:
            best_result = max(int(float(r[1].split(",")[15]) * 100), best_result)
        strr += "({"+result[0][0].split(",")[1]+"}, " +str(best_result) + ")\n"
    strr += """};
    \legend{CPAP,Other Treatment}
    \end{axis}
    \end{tikzpicture}
    
    """
    return strr