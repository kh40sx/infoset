#!/usr/bin/env python3

"""Demonstration Script that extracts agent data from cache directory files.

This could be a modified to be a daemon

"""

# Standard libraries
import os
import time
import json
import hashlib
from collections import defaultdict
import queue as Queue
import threading
import re

# Infoset libraries
from infoset.db import db
from infoset.db import agent

# Define a key global variable
THREAD_QUEUE = Queue.Queue()


class Drain(object):
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
            filename: Cache filename

        Returns:
            None

        """
        # Initialize key variables
        self.filename = filename
        self.data = defaultdict(lambda: defaultdict(dict))
        self.metadata = []
        self.agent_meta = {}
        data_types = ['chartable', 'other']
        agent_meta_keys = ['timestamp', 'uid', 'agent']

        # Ingest data
        with open(filename, 'r') as f_handle:
            information = json.load(f_handle)

        # Get universal parameters from file
        for key in agent_meta_keys:
            self.agent_meta[key] = information[key]
        timestamp = information['timestamp']
        uid = information['uid']

        # Process chartable data
        for data_type in data_types:
            for label, group in sorted(information[data_type].items()):
                # Get universal parameters for group
                base_type = _base_type(group['base_type'])
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
                        (uid, did, label, source, description, base_type)
                    )

    def uid(self):
        """Return uid.

        Args:
            None

        Returns:
            data: Agent UID

        """
        # Initialize key variables
        data = self.agent_meta['uid']

        # Return
        return data

    def timestamp(self):
        """Return timestamp.

        Args:
            None

        Returns:
            data: Agent timestamp

        """
        # Initialize key variables
        data = self.agent_meta['timestamp']

        # Return
        return data

    def agent(self):
        """Return agent.

        Args:
            None

        Returns:
            data: Agent agent_name

        """
        # Initialize key variables
        data = self.agent_meta['agent']

        # Return
        return data

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
        if 32 in self.data['chartable']:
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
        if 64 in self.data['chartable']:
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
        if 1 in self.data['chartable']:
            data = self.data['chartable']['gauge']
        else:
            data = []

        # Return
        return data

    def chartable(self):
        """Return all chartable data from file.

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

        # Initialize key variables
        for key in self.data['chartable'].keys():
            data.extend(self.data['chartable'][key])

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
                base_type = SNMP base type code (Counter32, Gauge etc.)

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
            success: "True" if successful

        """
        # Initialize key variables
        success = True

        try:
            os.remove(self.filename)
        except:
            success = False

        # Return
        return success


class FillDB(threading.Thread):
    """Threaded polling.

    Graciously modified from:
    http://www.ibm.com/developerworks/aix/library/au-threadingpython/

    """

    def __init__(self, queue):
        """Initialize the threads."""
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        """Update the database using threads."""
        while True:
            # Get the data_dict
            data_dict = self.queue.get()
            uid = data_dict['uid']
            metadata = data_dict['metadata']
            config = data_dict['config']
            agents = data_dict['agents']
            datapoints = data_dict['datapoints']

            # Sort metadata by timestamp
            metadata.sort()

            # Process file for each timestamp
            for (timestamp, filepath) in metadata:
                # Read in data
                ingest = Drain(filepath)

                # Double check that the UID and timestamp in the
                # filename matches that in the file
                if uid != ingest.uid():
                    continue
                if timestamp != ingest.timestamp():
                    continue

                # Update agent table if not there
                if ingest.uid() not in agents:
                    _insert_agent(
                        ingest.uid(),
                        ingest.agent(),
                        config
                        )
                    # Append the new insertion to the list
                    agents.append(ingest.uid())

                # Update datapoint metadata if not there
                for item in ingest.sources():
                    did = item[1]
                    if did not in datapoints:
                        _insert_datapoint(item, config)
                        # Append the new insertion to the list
                        datapoints.append(did)

                # Update chartable data
                _insert_gauge_data(ingest, config)

                # Purge source file
                ingest.purge()

            # All done!
            self.queue.task_done()


def _insert_gauge_data(ingest, config):
    """Insert data into the database "iset_data" table.

    Args:
        ingest: Drain object
        config: Config object

    Returns:
        None

    """
    # Initialize key variables
    data = ingest.chartable()
    data_list = []
    timestamp_tracker = {}

    # Create map of DIDs to database row index values
    mapping = _datapoints_by_did(config)

    # Update gauge data
    for item in data:
        # Process each datapoint item found
        (_, did, value, timestamp) = item
        idx_datapoint = mapping[did][0]
        idx_agent = mapping[did][1]
        last_timestamp = mapping[did][2]

        # Only update with data collected after
        # the most recent update
        if timestamp > last_timestamp:
            data_list.append(
                (idx_datapoint, idx_agent, value, timestamp)
            )

        # Update DID's last updated timestamp
        if idx_datapoint in timestamp_tracker:
            timestamp_tracker[idx_datapoint] = max(
                timestamp, timestamp_tracker[idx_datapoint])
        else:
            timestamp_tracker[idx_datapoint] = timestamp

    # Prepare SQL query to read a record from the database.
    sql_insert = (
        'REPLACE INTO iset_data '
        '(idx_datapoint, idx_agent, value, timestamp) VALUES '
        '(%s, "%s", %s, %s)')

    # Do query and get results
    database = db.Database(config)
    database.modify(sql_insert, 1096, data_list=data_list)

    # Change the last updated timestamp
    for idx_datapoint, last_timestamp in timestamp_tracker.items():
        # Prepare SQL query to read a record from the database.
        sql_modify = (
            'UPDATE iset_datapoint SET last_timestamp=%s '
            'WHERE iset_datapoint.idx=%s') % (last_timestamp, idx_datapoint)
        database.modify(sql_modify, 1096)


def _insert_datapoint(metadata, config):
    """Insert new datapoint into database.

    Args:
        metadata: Tuple of datapoint metadata.
            (uid, did, label, source, description)
            uid: Agent UID
            did: Datapoint ID
            label: Datapoint label created by agent
            source: Source of the data (subsystem being tracked)
            description: Description provided by agent config file (unused)
            base_type = SNMP base type (Counter32, Counter64, Gauge etc.)
        config: Configuration object

    Returns:
        None

    """
    # Initialize key variables
    (uid, did, label, source, _, base_type) = metadata

    # Get agent index value
    agent_object = agent.Get(uid, config)
    idx_agent = agent_object.idx()

    # Prepare SQL query to read a record from the database.
    sql_query = (
        'INSERT INTO iset_datapoint '
        '(id, idx_agent, agent_label, agent_source, base_type ) VALUES '
        '("%s", %d, "%s", "%s", %d)'
        '') % (did, idx_agent, label, source, base_type)

    # Do query and get results
    database = db.Database(config)
    database.modify(sql_query, 1074)


def _insert_agent(uid, name, config):
    """Insert new agent into database.

    Args:
        uid: Agent uid
        name: agent name

    Returns:
        None

    """
    # Prepare SQL query to read a record from the database.
    sql_query = (
        'INSERT INTO iset_agent (id, name) VALUES ("%s", "%s")'
        '') % (uid, name)

    # Do query and get results
    database = db.Database(config)
    database.modify(sql_query, 1074)


def _datapoints(config):
    """Create list of enabled datapoints.

    Args:
        config: Configuration object

    Returns:
        data: List of active datapoints

    """
    # Initialize key variables
    data = []

    # Prepare SQL query to read a record from the database.
    sql_query = (
        'SELECT iset_datapoint.id '
        'FROM iset_datapoint WHERE (iset_datapoint.enabled=1)')

    # Do query and get results
    database = db.Database(config)
    query_results = database.query(sql_query, 1074)

    # Massage data
    for row in query_results:
        data.append(row[0])

    # Return
    return data


def _datapoints_by_did(config):
    """Create dict of enabled datapoints and their corresponding indices.

    Args:
        config: Configuration object

    Returns:
        data: Dict keyed by datapoint ID,
            with a tuple as its value (idx, idx_agent)
            idx: Datapoint index
            idx_agent: Agent index
            last_timestamp: The last time the timestamp was updated

    """
    # Initialize key variables
    data = {}

    # Prepare SQL query to read a record from the database.
    sql_query = (
        'SELECT iset_datapoint.id, iset_datapoint.idx, '
        'iset_datapoint.idx_agent, iset_datapoint.last_timestamp '
        'FROM iset_datapoint WHERE (iset_datapoint.enabled=1)')

    # Do query and get results
    database = db.Database(config)
    query_results = database.query(sql_query, 1074)

    # Massage data
    for row in query_results:
        did = row[0]
        idx = row[1]
        idx_agent = row[2]
        last_timestamp = row[3]
        data[did] = (idx, idx_agent, last_timestamp)

    # Return
    return data


def _agents(config):
    """Create list of active agent UIDs.

    Args:
        config: Configuration object

    Returns:
        data: List of active agents

    """
    # Initialize key variables
    data = []

    # Prepare SQL query to read a record from the database.
    sql_query = (
        'SELECT iset_agent.id '
        'FROM iset_agent WHERE (iset_agent.enabled=1)')

    # Do query and get results
    database = db.Database(config)
    query_results = database.query(sql_query, 1074)

    # Massage data
    for row in query_results:
        data.append(row[0])

    # Return
    return data


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


def _base_type(data):
    """Create a base_type integer value from the string sent by agents.

    Args:
        data: base_type value as string

    Returns:
        base_type: Base type value as integer

    """
    # Initialize key variables
    if bool(data) is False:
        value = 'NULL'
    else:
        value = data

    # Assign base type code
    if value.lower() == 'gauge':
        base_type = 1
    elif value.lower() == 'counter32':
        base_type = 32
    elif value.lower() == 'counter64':
        base_type = 64
    else:
        base_type = 0

    # Return
    return base_type


def process(config):
    """Method initializing the class.

    Args:
        config: Configuration object

    Returns:
        None

    """
    # Initialize key variables
    threads_in_pool = config.ingest_threads()
    uid_metadata = defaultdict(lambda: defaultdict(dict))
    cache_dir = config.ingest_cache_directory()

    # Get a list of active agents and datapoints
    agents = _agents(config)
    datapoints = _datapoints(config)

    # Spawn a pool of threads, and pass them queue instance
    for _ in range(threads_in_pool):
        update_thread = FillDB(THREAD_QUEUE)
        update_thread.daemon = True
        update_thread.start()

    # Add files in cache directory to list
    all_filenames = [filename for filename in os.listdir(
        cache_dir) if os.path.isfile(
            os.path.join(cache_dir, filename))]

    ######################################################################
    # Create threads
    ######################################################################

    # Process only valid agent filenames
    for filename in all_filenames:
        # Filenames must start with a numeric timestamp and end with a hex
        # string
        regex = re.compile(r'^\d+_[0-9a-f]+.json')

        # Add valid data to lists
        if bool(regex.match(filename)) is True:
            # Create a complete filepath
            filepath = os.path.join(cache_dir, filename)

            # Only read files that are 5 seconds or older
            # to prevent corruption caused by reading a file that could be
            # updating simultaneously
            if time.time() - os.path.getmtime(filepath) < 5:
                continue

            # Create a dict of UIDs, timestamps and filepaths
            (name, _) = filename.split('.')
            (tstamp, uid) = name.split('_')
            timestamp = int(tstamp)
            if uid in uid_metadata:
                uid_metadata[uid].append(
                    (timestamp, filepath))
            else:
                uid_metadata[uid] = [(timestamp, filepath)]

    # Read each cache file
    for uid in uid_metadata.keys():

        ####################################################################
        #
        # Define variables that will be required for the threading
        # We have to initialize the dict during every loop to prevent
        # data corruption
        #
        ####################################################################
        data_dict = {}
        data_dict['uid'] = uid
        data_dict['metadata'] = uid_metadata[uid]
        data_dict['config'] = config
        data_dict['agents'] = agents
        data_dict['datapoints'] = datapoints
        THREAD_QUEUE.put(data_dict)

    # Wait on the queue until everything has been processed
    THREAD_QUEUE.join()

    # PYTHON BUG. Join can occur while threads are still shutting down.
    # This can create spurious "Exception in thread (most likely raised
    # during interpreter shutdown)" errors.
    # The "time.sleep(1)" adds a delay to make sure things really terminate
    # properly. This seems to be an issue on virtual machines in Dev only
    time.sleep(1)
