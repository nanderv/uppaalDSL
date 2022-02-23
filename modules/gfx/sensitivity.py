def sensitivity_table(results):
    rr = ""
    for result in results:
        params = result.keys.get("PROG","-")
        res = result.result_list
        if rr == "" or True:
            rr += params

        rr = rr + ", " + str(100 * float(res[1]) / (float(res[1]) + float(res[2]))) + "\n"

    return rr