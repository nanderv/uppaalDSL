from modules.runners.run import RunResult


def from_file(file, POPS):
    inputs = []
    with  open("output/results/" + file, "r") as my_file:
        line0 = None
        keys = []
        for z in my_file.readline().strip().split(","):
            keys.append(z)
        while line := my_file.readline():
            if line.strip() != "":
                if line0 is None:
                    line0 = line.strip()
                else:
                    line1 = line.strip()
                    new_result = RunResult(POPS)
                    it = 0
                    for a in line0.strip().split(","):
                        if a == "":
                            continue
                        new_result.add_param(keys[it], a)

                        it += 1
                    for b in line1.strip().split(","):
                        new_result.add_result(b, b)
                    inputs.append(new_result)
                    line0 = None

    return inputs