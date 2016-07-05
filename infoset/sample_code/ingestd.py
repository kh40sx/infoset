#!/usr/bin/env python3

"""Demonstration Script that extracts agent data from cache directory files.

This could be a modified to be a daemon

"""

# Standard libraries
import os
import json
from threading import Timer
import hashlib
import argparse
from collections import defaultdict
from pprint import pprint


class Ingest(object):
    """Infoset class that ingests agent data.

    Args:
        None

    Returns:
        None

    Methods:
        __init__:
        populate:
        post:
    """

    def __init__(self, filename):
        """Method initializing the class.

        Args:
            uid: Unique ID for Agent
            config: Configuration object

        Returns:
            None

        """
        # Initialize key variables
        self.filename = filename
        self.data = defaultdict(lambda: defaultdict(dict))
        self.metadata = []
        data_types = ['chartable', 'other']

        # Ingest data
        with open(filename, 'r') as f_handle:
            information = json.load(f_handle)

        pprint(information)

        # Get universal parameters from file
        timestamp = information['timestamp']
        uid = information['uid']

        # Process chartable data
        for data_type in data_types:
            for label, group in sorted(information[data_type].items()):
                # Get universal parameters for group
                base_type = group['base_type']
                description = group['description']

                # Initialize base type
                if base_type not in self.data[data_type]:
                    self.data[data_type][base_type] = []

                # Process data
                for datapoint in group['data']:
                    index = datapoint[0]
                    value = datapoint[1]
                    source = datapoint[2]
                    did = _did(uid, label, index)

                    # Update data
                    self.data[data_type][base_type].append(
                        (uid, did, value, timestamp)
                    )

                    # Update sources
                    self.metadata.append(
                        (uid, did, label, source, description)
                    )

    def counter32(self):
        """Return counter32 chartable data from file.

        Args:
            None

        Returns:
            data: List of tuples (uid, did, value, timestamp)
                uid = UID of device providing data
                did = Datapoint ID
                value = Value of datapoint
                timestamp = Timestamp when data was collected by the agent

        """
        # Initialize key variables
        if 'counter32' in self.data['chartable']:
            data = self.data['chartable']['counter32']
        else:
            data = []

        # Return
        return data

    def counter64(self):
        """Return counter64 chartable data from file.

        Args:
            None

        Returns:
            data: List of tuples (uid, did, value, timestamp)
                uid = UID of device providing data
                did = Datapoint ID
                value = Value of datapoint
                timestamp = Timestamp when data was collected by the agent

        """
        # Initialize key variables
        if 'counter64' in self.data['chartable']:
            data = self.data['chartable']['counter64']
        else:
            data = []

        # Return
        return data

    def gauge(self):
        """Return gauge chartable data from file.

        Args:
            None

        Returns:
            data: List of tuples (uid, did, value, timestamp)
                uid = UID of device providing data
                did = Datapoint ID
                value = Value of datapoint
                timestamp = Timestamp when data was collected by the agent

        """
        # Initialize key variables
        if 'gauge' in self.data['chartable']:
            data = self.data['chartable']['gauge']
        else:
            data = []

        # Return
        return data

    def other(self):
        """Return other non-chartable data from file.

        Args:
            None

        Returns:
            data: List of tuples (uid, did, value, timestamp)
                uid = UID of device providing data
                did = Datapoint ID
                value = Value of datapoint
                timestamp = Timestamp when data was collected by the agent

        """
        # Initialize key variables
        data = []

        # Return (Ignore whether gauge or counter)
        for _, value in self.data['other'].items():
            data.extend(value)
        return data

    def sources(self):
        """Return sources data from file.

        Args:
            None

        Returns:
            data: List of tuples (uid, did, label, source, description)
                uid = UID of device providing data
                did = Datapoint ID
                label = Label that the agent gave the category of datapoint
                source = Subsystem that provided the data in the datapoint
                description = Description of the label

        """
        # Initialize key variables
        data = self.metadata

        # Return
        return data

    def purge(self):
        """Purge cache file that was read.

        Args:
            None

        Returns:
            success: "True: if successful

        """
        # Initialize key variables
        success = True

        try:
            os.remove(self.filename)
        except:
            success = False

        # Return
        return success


def _did(uid, label, index):
    """Create a unique DID from ingested data.

    Args:
        uid: UID of device that created the cache data file
        label: Label of the data
        index: Index of the data

    Returns:
        did: Datapoint ID

    """
    # Initialize key variables
    prehash = ('%s%s%s') % (uid, label, index)
    hasher = hashlib.sha256()
    hasher.update(bytes(prehash.encode()))
    did = hasher.hexdigest()

    # Return
    return did


def ingest(cache_dir):
    """Ingest agent data from cache directory.

    Args:
        cache_dir: Cache directory with agent data

    Returns:
        None

    """
    # Add files in cache directory to list
    filenames = [filename for filename in os.listdir(
        cache_dir) if os.path.isfile(
            os.path.join(cache_dir, filename))]

    #########################################################################
    # This could be threaded on a per file basis
    #########################################################################

    # Read each cache file
    for filename in filenames:
        filepath = os.path.join(cache_dir, filename)

        # Process data
        get = Ingest(filepath)

        #####################################################################
        # We will need to keep track of the previous value of counter data
        # for each DID and then subtract one from the other to get
        # incremental values.
        #
        # If there is no previous value, then assume this is the first.
        #
        # We will have to only subtract between timestamps that are 300
        # seconds apart to ensure accuracy.
        #
        # We will have to determine whether the counter has rolled over and
        # take this into consideration
        #
        #####################################################################
        # Get counter information
        pprint(get.counter32())
        print('\n\n\n')
        pprint(get.counter64())

        # Get other information
        print('\n\n\n')
        pprint(get.gauge())
        print('\n\n\n')
        pprint(get.other())
        print('\n\n\n')
        pprint(get.sources())
        print('\n\n\n')

        #####################################################################
        # Purge file so that we don't use it again
        #####################################################################

        # get.purge()

        #####################################################################
        # Put data in relevant database tables
        #####################################################################


def process_cli(additional_help=None):
    """Return all the CLI options.

    Args:
        None

    Returns:
        args: Namespace() containing all of our CLI arguments as objects
            - filename: Path to the configuration file

    """
    # Header for the help menu of the application
    parser = argparse.ArgumentParser(
        description=additional_help,
        formatter_class=argparse.RawTextHelpFormatter)

    # CLI argument for the config directory
    parser.add_argument(
        '--cache_dir',
        dest='cache_dir',
        required=True,
        default=None,
        type=str,
        help='Cache directory with agent data.'
    )

    # Return the CLI arguments
    args = parser.parse_args()

    # Return our parsed CLI arguments
    return args


def main():
    """Process agent data.

    Args:
        None

    Returns:
        None

    """
    # Get configuration
    args = process_cli()

    # Get data from the cache directory
    ingest(args.cache_dir)

    # Do the daemon thing
    Timer(10, main).start()


if __name__ == "__main__":
    main()
