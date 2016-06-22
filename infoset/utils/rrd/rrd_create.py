from infoset.utils.rrd.modules.cpu_percentage import Cpu_Percentage
import threading
import rrdtool
import queue as Queue

THREAD_QUEUE = Queue.Queue()


class RrdCreateAgent(threading.Thread):

    def __init__(self, content, device_root_path):
        threading.Thread.__init__(self)
        self.content = content
        self.path = device_root_path

    def run(self):
        while True:
            print("From thread")


def parse(content, device_folder):
    for key, value in content.copy().items():
        if key == "cpu_percentage":
            cpu_rrd = Cpu_Percentage(root=device_folder, step=300)
            cpu_rrd.appendDataSource(variable_name="cpu_percentage", type="gauge", heartbeat=300)
            del content["cpu_percentage"]
            print("from loop")

