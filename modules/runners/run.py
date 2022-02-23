import subprocess

from conf import VERIFYTA_PATH


class RunResult:

    def __init__(self, pops=1):
        self.keys = {}
        self.param_key_list = []
        self.param_list = []
        self.result_list = []
        self.add_param("POPS", pops)

    def add_param(self, param, data):
        self.param_list.append(data)
        if param not in self.keys.keys():
            self.keys[param] = data
        self.param_key_list.append(param)

    def add_result(self, param, data):
        self.result_list.append(data)
        self.keys[param] = data

    def __str__(self):
        ret = "Params:\n"
        for p in self.param_list:
            ret += str(p) + "\n"
        ret += "Results:  \n"
        for p in self.result_list:
            ret += str(p) + "\n"
        return ret


def run(input_xml, input_q, base_var, lstlsts, config):
    result = subprocess.run([VERIFYTA_PATH, input_xml, input_q], stdout=subprocess.PIPE)
    resultObj = RunResult()
    for z in lstlsts:
        resultObj.add_param(z.param, z.get_value_name())
    i = 0
    for line in str(result.stdout).split("\\n"):
        i += 1
        if " runs)" in line:
            if "Pr" in line:
                y = line.split("in [")[-1].strip()
                y = y.split("]")[0].strip()
                y = y.split(",")
                a, b = float(y[0]), float(y[1])
                resultObj.add_result("P" + str(i), (a + b) / 2)
            if "E" in line:
                z = float(line.split("=")[-1].strip())
                resultObj.add_result("P" + str(i), z)
    return resultObj
