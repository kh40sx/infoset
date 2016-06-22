import rrdtool
import time

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
    def __init__(self, root, filename, step=300, start=int(time.time()), data_sources=[], rras=[]):
        self.root = str(root)
        self.filename = str(filename)
        self.step = step
        self.start = start
        self.data_sources = data_sources
        self.rras = rras


    def setFilename(self, filename):
        self.filename = filename

    def getFilename(self):
        return self.filename

    def setRoot(self, root):
        self.root = root

    def getRoot(self):
        return self.root

    def appendDataSource(self, variable_name, type, heartbeat):
        data_source = "DS:%s:%s:%s:U:U" % (variable_name, type.upper(), heartbeat)
        self.data_sources.append(data_source)

    def appendRoundRobinArchive(self, cf, xff, steps, rows):
        rra = "RRA:%s:%s:%s:%s" % (cf.upper(), xff, steps, rows)
        self.rras.append(rra)

    def create(self):
        print("info: %.rrd created in %s" % (self.filename, self.root))
        timestamp = self.normalized_timestamp(time.time(), self.step)
        rrdtool.create(
            '%s/%s.rrd' % (self.device_root, self.filename),
            '--step', str(self.step),
            '--start', str(timestamp),
            self.data_sources,
            self.rras)

    def update(self, data):
        rrdtool.update(
            './infoset/utils/rrd/' + self.filename,
            ('%s:%s') % (str(int(time.time())), data)
        )

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