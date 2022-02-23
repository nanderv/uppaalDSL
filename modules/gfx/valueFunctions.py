def get_sensitivity(res):
    return 100 * float(res[1]) / (float(res[1]) + float(res[2]))


def get_specificity(res):
    return 100 * float(res[3]) / (float(res[3]) + float(res[4]))


def get_costs(res):
    return float(res[5])


def get_costs_per(res):
    return float(res[5]) / float(res[1])


def get_NPV(res):
    return float(res[3])/(float(res[3]) + float(res[2]))


def get_PPV(res):
    return float(res[1]) / (float(res[1]) + float(res[4]))
