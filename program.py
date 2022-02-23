import sys
import threading
import time

import tqdm as tqdm

from modules.runners.run import run
from modules.simulation.config import load_config, load_sim_xml
from modules.transformations.parseparams import parse_file
from modules.transformations.transform import transform_UPPAAL

N_WORKERS = 3
WORKERS = []

class Worker(threading.Thread):
    ID = 0

    def __init__(self):
        super().__init__()
        self.UUID = Worker.ID
        self.result = None
        Worker.ID = (Worker.ID + 1)%(N_WORKERS + 1)
        self.res = None
        self.lstlst = None

    def set_params(self, res, lstlst):
        self.res = res
        self.lstlst = lstlst

    def run(self):
        res = self.res
        lstlst = self.lstlst
        transform_UPPAAL(res.xml, lstlst)
        res.xml.write("output/" + str(self.UUID) + res.config.output)
        z = (run("output/" + str(self.UUID) + res.config.output, "uppaal/" + config.query, res.program_name, lstlst, config))
        self.result = z


class DataStore:
    ADT = False
    DDT = False

    @staticmethod
    def get_should_ADT():
        return DataStore.ADT

    @staticmethod
    def get_should_DDT():
        return DataStore.DDT


folder = "basic/1"
mode = "EXP"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    print(folder)
    # print("Simulating " + folder)
    config = load_config(folder)
    opts = parse_file(folder)
    c = 0
    res = 0


    def exp(data):
        from modules.export.adt import export
        return export(data)


    def get_key(res, z, lst, ignore):
        rz = ""
        if "ddt" in ignore:
            z = ""

        if "pname" not in ignore:
            rz = res.program_name + ":" + z + ":"

        for mz in lst:
            not_in = False

            for rz in ignore:
                if rz not in mz.param:
                    not_in = True

            if not not_in:
                rz += (":" + str(mz.value_name))
        return rz


    all_results = []

    if mode == "EXP":
        counter = 0
        ended = 0
        print(len(opts))
        for a in tqdm.tqdm(opts):

            counter += 1
            # print(counter)
            res = load_sim_xml(config)
            my_key = 1
            if res is not None:
                    if len(WORKERS) < N_WORKERS:
                        b = list(a)
                        worker = Worker()
                        worker.set_params(res, b)
                        worker.start()
                        WORKERS.append(worker)
                    else:
                        while WORKERS[0].is_alive():
                            time.sleep(1)
                        worker =  WORKERS.pop(0)
                        my_key += 1
                        ended += 1
                        all_results.append(worker.result)
                        worker.result = None

                        b = list(a)
                        worker = Worker()
                        worker.set_params(res, b)
                        worker.start()
                        WORKERS.append(worker)
        while len(WORKERS) > 0:
            while WORKERS[0].is_alive():
                time.sleep(1)
                sys.stdout.flush()
            worker = WORKERS.pop(0)
            my_key += 1
            ended += 1
            all_results.append(worker.result)
            worker.result = None
            sys.stdout.flush()
        f = open("output/results/" + folder + ".txt", "w")

        rr = ""
        for a in all_results[0].param_key_list:
            rr += str(a)
            rr += ","
        for line in all_results:
            rr += "\n"
            for it in line.param_list:
                if isinstance(it, float):
                    rr += str(format(it, 'f')) + ","
                else:
                    rr += str(it) + ","
            rr += "\n"
            for it in line.result_list:
                if isinstance(it, float):
                    rr += str(format(it,'f')) + ","
                else:
                    rr += str(it) + ","
            f.write(rr)
            f.flush()
            rr = ""
        f.close()

