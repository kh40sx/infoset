import threading
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
    for item in content.items():
        print(item)