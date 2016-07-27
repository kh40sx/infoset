import time

class TimeStamp(object):
    def __init__(self):
        self.presets = [1800, 3600, 10800, 18000, 28800, 43200]
        self.descriptions = ["Five Minute", "Thirty Minute", "One Hour", "Three Hours", "Eight Hours", "Twelve Hours"]
        self.doTimes()
    
    def doTimes(self):
        now = int(time.time())
        self.start_times = []
        self.stop_times = []
        for timestamp in self.presets:
            start = now - timestamp
            self.start_times.append(start)
            self.stop_times.append(now)
        self.times = zip(self.start_times, self.stop_times, self.descriptions)

    def getTimes(self):
        value = self.times
        return value
