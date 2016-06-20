
import getpass
import time
import datetime
import textwrap
import argparse
import pwd
import grp
import os
import sys
import psutil
import rrdtool
import threading

__author__ = 'Peter Harrison (Colovore LLC.) <peter@colovore.com>'
__version__ = '0.0.1'


class RrdUpdateAgent(threading.Thread):

    """Docstring for RrdAgent. """

    def __init__(self, filename, step, type):
        """TODO: to be defined1. """
        self.filename = filename
        self.step = step
        self.type = type

    def create(self):
        """Create RRD file.

        Args:
            cli_args: CLI arguments object

        Returns:
            None

        """
        # Initialize key variables
        timestamp = self.normalized_timestamp(int(time.time()),
                                              rrd_step=self.step)
        print(timestamp)
        # Create data sources and definitions
        data_sources = [('DS:data_00:GAUGE:%s:U:U') % (self.step)]
        rra_definitions = [
            'RRA:AVERAGE:0.5:1:288',
            'RRA:AVERAGE:0.5:6:10',
            'RRA:MAX:0.5:1:24',
            'RRA:MAX:0.5:6:10']

        # Print
        output = (
            'Creating file %s. File can only be created in '
            'RRDcached base directory.') % (self.filename)
        print(output)

        # Create file
        rrdtool.create(
            './infoset/utils/rrd/%s' % (self.filename),
            '--step', str(self.step),
            '--start', str(int(time.time())),
            data_sources,
            rra_definitions)
        self.startTime = int(time.time())

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

    def update(self, data):
        """Update RRD file.

        Args:
            cli_args: CLI arguments object
            Returns:
                None

        """

        timestamp = self.normalized_timestamp(int(time.time()),
                                              rrd_step=self.step)
        # Initialize key variables

        # Create an integer value based on today's date

        # Data
        data = ('%s:%s') % (timestamp, 5)

        # Print
        output = (
            'Updating file %s with value %s at timestamp %s. '
            'File can only be created in RRDcached base directory.'
            '') % (self.filename, data, timestamp)
        print(output)

        # Update file
        rrdtool.update(
            './infoset/utils/rrd/' + self.filename,
            ('%s:%s') % (timestamp, data)
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
