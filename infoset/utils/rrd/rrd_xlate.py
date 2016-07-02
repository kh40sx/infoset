from os import walk, path, listdir, remove
import yaml
from infoset.utils.rrd.modules.rrd import Rrd


class RrdXlate():
    def __init__(self, root):
        self.root = root

    def rrd_update(self):
        directories = [d for d in listdir(self.root) if path.isdir(path.join(self.root, d))]
        for directory in directories:
            active_yaml = self.root + directory + str("/active.yaml")
            directory_root = self.root + directory
            with open(active_yaml, 'r') as stream:
                try:
                    active_yaml = yaml.load(stream)
                    for key, value in active_yaml['chartable'].items():
                        rrd = Rrd(directory_root, key)
                        rrd.appendDataSource("data_00", "gauge", "600")
                        rrd.appendRoundRobinArchive("average", "0.5", "1", "288")
                        rrd.appendRoundRobinArchive("average", "0.5", "6", "10")
                        rrd.appendRoundRobinArchive("max", "0.5", "1", "24")
                        rrd.appendRoundRobinArchive("max", "0.5", "6", "10")
                        rrd.update(value)
                except Exception as e:
                    raise e

    def rrd_graph(self):
        # Device folder containing rrd files
        # Get current device folder then get all files
        for file in listdir(self.root):
            if file.endswith(".png"):
                remove(self.root + "/" +file)

        for file in listdir(self.root):
            if file.endswith(".rrd"):
                rrd = Rrd(self.root, file[:-4])
                rrd.graph()