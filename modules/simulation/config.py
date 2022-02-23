import importlib
import xml.etree.ElementTree

# from modules.generate_uppaal.graphFormatToUppaal import to_uppaal
#
# from modules.generate_uppaal.importGraphFormat import import_graph, DdtNode, AdtNode


class Config:
    def __init__(self):
        self.model = None
        self.output = None
        self.query = None

    def __str__(self):
        strr = self.model + " ==> " + self.output + "::\ninternal:\n"
        return strr


class RunProfile:
    def __init__(self, xml, config):
        self.xml = xml
        self.config = config
        self.profile_name = ""
        self.program_name = ""


def load_config(c: str):
    config = Config()
    with  open('simulations/' + c + "/config.txt", "r") as my_file:
        while line := my_file.readline().strip():
            l = line.split(":")
            cmd = l[0]
            if cmd == "model":
                config.model = l[1].strip()
            if cmd == "output":
                config.output = l[1].strip()
            if cmd == "query":
                config.query = l[1].strip()
    return config


def load_sim_xml(c: Config):
    tree = xml.etree.ElementTree.parse("uppaal/" + c.model)
    return RunProfile(tree, c)
