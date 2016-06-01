
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
# Install using the command
# "pip3 install rrdtool==0.1.1" Xenial version is buggy.
import rrdtool

__author__ = 'Peter Harrison (Colovore LLC.) <peter@colovore.com>'
__version__ = '0.0.1'


class RrdAgent():

    """Docstring for RrdAgent. """

    def __init__(self, filename, step):
        """TODO: to be defined1. """
        self.filename = filename
        self.step = step
        self.socket = 'unix:/var/run/rrdcached.sock'

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
            'RRA:AVERAGE:0.5:1:24',
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
            '--daemon', self.socket,
            '--step', str(self.step),
            '--start', str(timestamp),
            data_sources,
            rra_definitions)

    def graph(self):
        rrdtool.graph('./www/static/img/graph.png',
                      '--imgformat', 'PNG',
                      '--width', '540',
                      '--height', '100',
                      '--vertical-label', 'Percentage',
                      '--title', 'CPU Usage',
                      '--lower-limit', '0',
                      ('DEF:data=./infoset/utils/rrd/%s:data_00:AVERAGE') % self.filename,
                      'LINE.5:data#000000')

    def update(self):
        """Update RRD file.

        Args:
            cli_args: CLI arguments object
            Returns:
                None

        """

        timestamp = self.normalized_timestamp(int(time.time()),
                                              rrd_step=self.step)
        cpu_percent = psutil.cpu_percent(interval=1)
        # Initialize key variables

        # Create an integer value based on today's date

        # Data
        data = ('%s:%s') % (timestamp, cpu_percent)

        # Print
        output = (
            'Updating file %s with value %s at timestamp %s. '
            'File can only be created in RRDcached base directory.'
            '') % (self.filename, data, timestamp)
        print(output)

        # Update file
        rrdtool.update(
            self.filename,
            '--daemon', self.socket,
            data
        )

    def rrd_metadata(cli_args):
        """Return rrd metadata.

        Args:
            cli_args: CLI arguments object

        Returns:
            metadata: Metadata

        """
        # Initialize key variables
        rrd_step = 5
        base_directory = './'
        filename = ('%s/%s') % (
            base_directory.rstrip('/'),
            os.path.basename(cli_args.filename))
        time = int(time.time())
        timestamp = normalized_timestamp(time, 5)
        # Create metadata
        metadata = {
            'rrd_socket': 'unix:/var/run/rrdcached.sock',
            'rrd_step': rrd_step,
            'timestamp': timestamp,
            'filename': filename
        }
        return metadata

    def get_cli(additional_help=None):
        """Return all the CLI options.

        Args:
            None

        Returns:
            args: Namespace() containing all of our CLI arguments as objects
            - filename: Path to the configuration file

        """
        # Initialize key variables
        width = 80

        # Header for the help menu of the application
        parser = argparse.ArgumentParser(
            description=additional_help,
            formatter_class=argparse.RawTextHelpFormatter)

        # Add subparser
        subparsers = parser.add_subparsers(dest='mode')

        # Parse "create", return object used for parser
        cli_create(subparsers, width=width)

        # Parse "update", return object used for parser
        cli_update(subparsers, width=width)

        # Return the CLI arguments
        args = parser.parse_args()

        # Return our parsed CLI arguments
        return args

    def cli_create(subparsers, width=80):
        """Process local CLI commands.

        Args:
            subparsers: Subparsers object
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        parser = subparsers.add_parser(
            'create',
            help=textwrap.fill(
                'Create RRD file.', width=width)
        )

        # CLI argument for the config directory
        parser.add_argument(
            '--filename',
            dest='filename',
            required=True,
            default=None,
            type=str,
            help=textwrap.fill(
                'File to create.', width=width)
        )

    def cli_update(subparsers, width=80):
        """Process update CLI commands.

        Args:
            subparsers: Subparsers object
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        parser = subparsers.add_parser(
            'update',
            help=textwrap.fill(
                'Recursively SCP copy files to this '
                'server from a remote one.', width=width)
        )

        # CLI argument for the config directory
        parser.add_argument(
            '--filename',
            dest='filename',
            required=True,
            default=None,
            type=str,
            help=textwrap.fill(
                'File to update.', width=width)
        )

    def log2die(self, code=None, message=None, die=True):
        """Log message to screen and die.

        Args:
            code: Error code
            message: Error message

        Returns:
            None

        """
        # Initialize key variables
        app_name = 'daily_backup'
        username = getpass.getuser()
        time_object = datetime.datetime.fromtimestamp(time.time())
        timestring = time_object.strftime('%Y-%m-%d %H:%M:%S,%f')

        # Format string for error message
        prefix = ('%s - %s - DEBUG') % (timestring, app_name)
        suffix = ('[%s] (%s): %s') % (username, code, message)

        if die is True:
            # Print and die
            error = ('%s - ERROR - %s') % (prefix, suffix)
            print(error)
            sys.exit(2)
        else:
            # Append to backup file
            error = ('%s - STATUS - %s') % (prefix, suffix)
            print(error)

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
