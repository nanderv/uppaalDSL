from modules.gfx.valueFunctions import get_NPV


def npv_table(results):
    rr = ""
    for result in results:
        params = result.keys.get("PROG","-")
        res = result.result_list
        if rr == "" or True:
            rr += params

        rr = rr + ", " + str(get_NPV(res)) + "\n"

    return rr