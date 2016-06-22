import rrdtool
import time
from infoset.utils.rrd.modules.rrd import Rrd

class Cpu_Percentage(Rrd):
    def __init__(self, root, step, start=int(time.time())):
        super().__init__(root=root, filename="cpu_percentage", step=step, start=start, data_sources=[], rras=[])

    def graph(self):
        rrdtool.graph(('./www/static/img/%s.png') % (self.filename),
                      '--width', '540',
                      '--height', '100',
                      '--start', ('%s') % str(self.startTime),
                      '--vertical-label', 'Percentage',
                      '--title', 'CPU Usage',
                      '--lower-limit', '0',
                      ('DEF:data=./infoset/utils/rrd/%s:data_00:AVERAGE') % self.filename,
                      'LINE.5:data#000000')
