def waiting_table(results):
    rr = ""
    for result in results:
        if rr == "":
            rr += result.keys.get("PROG", "-")

        rr = rr + ", " + str(float(result.result_list[6]))
    return rr