import rrdtool
import time
from os import path


class Rrd():
    """Create RRD file.
    params:
        step: number
        start: time
        data sources: list
        rra: list
    Args:
        cli_args: CLI arguments object

    Returns:
        None

    """

    def __init__(self, root, filename, step=300, start=int(time.time())):
        self.root = str(root)
        self.filename = str(filename)
        self.step = step
        self.start = start
        self.data_sources = []
        self.rras = []

        # Causes bugs if removed, TODO fix
        # self.data_sources.append(data_sources)
        # self.rras.append(rras)

    def appendDataSource(self, variable_name, type, heartbeat):
        data_source = "DS:%s:%s:%s:U:U" % (variable_name, type.upper(), heartbeat)
        self.data_sources.append(data_source)

    def appendRoundRobinArchive(self, cf, xff, steps, rows):
        rra = "RRA:%s:%s:%s:%s" % (cf.upper(), xff, steps, rows)
        self.rras.append(rra)

    def create(self):
        print("info: %.rrd created in %s" % (self.filename, self.root))
        timestamp = self.normalized_timestamp(time.time(), self.step)
        self.startTime = timestamp

        rrdtool.create(
            '%s/%s.rrd' % (self.root, self.filename),
            '--step', str(self.step),
            '--start', str(timestamp),
            self.data_sources,
            self.rras)

    def update(self, data):
        filepath = self.root + "/" + self.filename + ".rrd"

        if not path.exists(filepath):
            self.create()
        rrdtool.update(
            filepath,
            '%s:%s' % (str(int(time.time())), data)
        )
        self.graph()

    def graph(self, color="1daad5"):
        rrdtool.graph(('%s/%s.png') % (self.root, self.filename),
                      '--width', '1233',
                      '--height', '369',
                      '-Y',
                      '-c', 'GRID#ffffff',
                      '-c', 'SHADEA#EEEEEE00',
                      '-c', 'SHADEB#EEEEEE00',
                      '-c', 'MGRID#FF9999',
                      '--font', 'TITLE:18:Hermit',
                      '--font', 'AXIS:14:Hermit',
                      '--title', '%s' % self.filename,
                      '--lower-limit', '0',
                      'DEF:data=%s/%s.rrd:data_00:AVERAGE' % (self.root, self.filename),
                      'AREA:data#%s' % color)

    def normalized_timestamp(self, timestamp, rrd_step=300):
        """Normalize the timestamp to a rrd_step boundary.

        Args:
            timestamp: timestamp to normalize
            rrd_step: Incremental time in seconds between RRD file updates.

        Returns:
            rrd_timestamp: The normalized timestamp

        """
        # Initialize key variables
        rrd_timestamp = 0

        # Normalize (The // operator trims remainers from results)
        if timestamp != 0:
            rrd_timestamp = int(timestamp // rrd_step) * rrd_step

        # Return
        return rrd_timestamp
