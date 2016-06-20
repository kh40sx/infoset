from os import walk, path
import yaml
from infoset.utils.rrd import rrd_create
import infoset.utils.rrd.rrd_update

class RrdCheck():
    def __init__(self, device_folder):
        self.root = device_folder

    def check(self):
        for root, directories, files in walk(self.root):
            for filename in files:
                if filename.endswith(".rrd"):
                    # Update rrds
                    print(filename)
                    break
            else:
                # Creates rrds
                # Get active yaml file
                active_yaml = self.root + str("/active.yaml")
                with open(active_yaml, 'r') as stream:
                    try:
                        active_yaml = yaml.load(stream)
                    except Exception as e:
                        raise e
                print("rrd does not exist, creating rrds")
                rrd_create.parse(active_yaml, self.root)