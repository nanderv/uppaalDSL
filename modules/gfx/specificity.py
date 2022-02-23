def specificity_table(results):
    rr = ""
    for result in results:
        params = result.keys.get("PROG","-")
        res = result.result_list
        if rr == "":
            rr += params

        rr = rr + ", " + str(100*float(res[3]) / (float(res[3])+float(res[4])))
    return rr