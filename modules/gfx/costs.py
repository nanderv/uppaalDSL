def cost_table(results, per=False):
    rr = ""
    for result in results:
        params = result.keys
        if rr == "":
            rr += params.get('PROG', "")
        if per:
            rr = rr + ", " + str(float(result.result_list[5]) / float(result.result_list[1]))
        else:
            rr = rr + ", " + str(float(result.result_list[5]))
    return rr