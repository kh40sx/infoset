
class ColorWheel(object):
    def __init__(self, agent_label):
        self.agent_label = agent_label
        self.color_palette = {
            "memory": "#00c8a4",
            "disk": "#0291D9",
            "load": "#f37372",
            "cpu": "#009DB2",
            "network": "#025AD9",
        }
        self.memory_stacked = ["#00c8a4", "#0291D9", "#f37372", "#009DB2", "#025AD9"]
        self.network_stacked = ["#00c8a4", "#0291D9", "#f37372", "#009DB2", "#025AD9"]
    
    def getScheme(self):
        if "memory" in self.agent_label:
            return self.color_palette["memory"]
        elif "disk" in self.agent_label:
            return self.color_palette["disk"]
        elif "network" in self.agent_label:
            return self.color_palette["network"]
        elif "load" in self.agent_label:
            return self.color_palette["load"]
        elif "cpu" in self.agent_label:
            return self.color_palette["cpu"]

    def getPalette(self):
        if "memory" in self.agent_label:
            return self.memory_stacked
        
