#!/usr/bin/env python3

"""Demonstration Script that extracts agent data from cache directory files.

This could be a modified to be a daemon

"""

# Standard libraries
import os
import time
import shutil
from collections import defaultdict
import queue as Queue
import re

# PIP libraries
from sqlalchemy import and_

# Infoset libraries
from infoset.db import db
from infoset.db.db_orm import Data, Datapoint, Agent, Host, HostAgent
from infoset.db import db_agent as agent
from infoset.db import db_datapoint as dpoint
from infoset.db import db_host as dhost
from infoset.db import db_hostagent as hagent
from infoset.utils import jm_configuration
from infoset.utils import jm_general
from infoset.utils import log
from infoset.utils.log import LogThread
from infoset.cache import drain
from infoset.utils import hidden

# Define a key global variable
THREAD_QUEUE = Queue.Queue()


class ProcessUID(LogThread):
    """Threaded ingestion of agent files.

    Graciously modified from:
    http://www.ibm.com/developerworks/aix/library/au-threadingpython/

    """

    def __init__(self, queue):
        """Initialize the threads."""
        LogThread.__init__(self)
        self.queue = queue

    def run(self):
        """Update the database using threads."""
        while True:
            # Initialize key variables
            hostname = None

            # Get the data_dict
            data_dict = self.queue.get()
            uid = data_dict['uid']
            metadata = data_dict['metadata']
            config = data_dict['config']

            # Initialize other values
            max_timestamp = 0

            # Sort metadata by timestamp
            metadata.sort()

            # Process file for each timestamp, starting from the oldes file
            for (timestamp, filepath) in metadata:
                # Get start time for activity
                start_ts = time.time()

                # Read in data
                ingest = drain.Drain(filepath)

                # Make sure file is OK
                # Move it to a directory for further analysis
                # by administrators
                if ingest.valid() is False:
                    log_message = (
                        'Cache ingest file %s is invalid. Moving.'
                        '') % (filepath)
                    log.log2warn(1054, log_message)
                    shutil.copy(
                        filepath, config.ingest_failures_directory())
                    os.remove(filepath)
                    continue

                # Update database
                dbase = UpdateDB(ingest)
                dbase.update()

                # Get the max timestamp
                max_timestamp = max(timestamp, max_timestamp)

                # Get hostname
                hostname = ingest.hostname()

                # Purge source file
                ingest.purge()

                # Log duration of activity
                duration = time.time() - start_ts
                log_message = (
                    'Cache ingest file %s was processed in %s seconds.'
                    '') % (filepath, round(duration, 4))
                log.log2quiet(1127, log_message)

            # Update the last time the agent was contacted
            _update_agent_last_update(uid, max_timestamp)

            # Update the host / agent table timestamp if hostname was processed
            if hostname is not None:
                _host_agent_last_update(hostname, uid, max_timestamp)

            # All done!
            self.queue.task_done()


class UpdateDB(object):
    """Update database with agent data."""

    def __init__(self, ingest):
        """Instantiate the class.

        Args:
            ingest: Drain object

        Returns:
            None

        """
        self.ingest = ingest

    def update(self):
        """Update the database.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        uid = self.ingest.uid()
        hostname = self.ingest.hostname()

        # Update Agent, Host and HostAgent database tables if
        # Host and agent are not already there
        self._insert_agent()
        self._insert_host()

        # Update datapoints if agent is enabled
        agent_object = agent.GetUID(uid)
        if agent_object.enabled() is True:
            # Get Agent and Host indexes
            idx_agent = agent_object.idx()

            # Get idx of host
            host_info = dhost.GetHost(hostname)
            idx_host = host_info.idx()

            # Update datapoint metadata if not there
            for item in self.ingest.sources():
                did = item[1]

                # We need the host that the data was generated for
                # and the agent that got the data
                if dpoint.did_exists(did) is False:
                    _insert_datapoint(item, idx_agent, idx_host)

            # Create map of DIDs to database row index values
            mapping = _datapoints_by_did(idx_agent)

            # Update chartable data
            self._update_chartable(mapping)
            self._update_unchartable(mapping)

    def _insert_agent(self):
        """Insert new agent into database.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        uid = self.ingest.uid()
        agent_name = self.ingest.agent()

        # Return if agent already exists in the table
        if agent.uid_exists(uid) is True:
            return

        # Prepare SQL query to read a record from the database.
        record = Agent(
            id=jm_general.encode(uid),
            name=jm_general.encode(agent_name))
        database = db.Database()
        database.add(record, 1081)

    def _insert_host(self):
        """Insert new agent into database.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        uid = self.ingest.uid()
        hostname = self.ingest.hostname()

        # Update Host table
        if dhost.hostname_exists(hostname) is False:
            # Add to Host table
            record = Host(hostname=jm_general.encode(hostname))
            database = db.Database()
            database.add(record, 1080)

        # Get idx of host
        host_info = dhost.GetHost(hostname)
        idx_host = host_info.idx()

        # Get idx of agent
        uid_info = agent.GetUID(uid)
        idx_agent = uid_info.idx()

        # Update HostAgent table
        if hagent.host_agent_exists(idx_host, idx_agent) is False:
            # Add to HostAgent table
            record = HostAgent(idx_host=idx_host, idx_agent=idx_agent)
            database = db.Database()
            database.add(record, 1038)

    def _update_chartable(self, mapping):
        """Insert data into the database "iset_data" table.

        Args:
            mapping: Map of DIDs to database row index values

        Returns:
            None

        """
        # Initialize key variables
        data = self.ingest.chartable()
        data_list = []
        timestamp_tracker = {}

        # Update data
        for item in data:
            # Process each datapoint item found
            (_, did, string_value, timestamp) = item
            idx_datapoint = int(mapping[did][0])
            last_timestamp = int(mapping[did][2])
            value = float(string_value)

            # Only update with data collected after
            # the most recent DID update. Don't do anything more
            if timestamp > last_timestamp:
                data_list.append(
                    Data(
                        idx_datapoint=idx_datapoint,
                        value=value,
                        timestamp=timestamp
                    )
                )

                # Update DID's last updated timestamp
                if idx_datapoint in timestamp_tracker:
                    timestamp_tracker[idx_datapoint] = max(
                        timestamp, timestamp_tracker[idx_datapoint])
                else:
                    timestamp_tracker[idx_datapoint] = timestamp

        # Update if there is data
        if bool(data_list) is True:
            # Do performance data update
            database = db.Database()
            success = database.add_all(data_list, 1056, die=False)

            # Change the last updated timestamp
            if success is True:
                # Create a database session
                # NOTE: We only do a single commit on the session.
                # This is much faster (20x based on testing) than
                # instantiating the database, updating records, and committing
                # after every iteration of the "for loop"
                database = db.Database()
                session = database.session()

                # Update the session
                for idx_datapoint, last_timestamp in timestamp_tracker.items():
                    data_dict = {'last_timestamp': last_timestamp}
                    session.query(Datapoint).filter(
                        Datapoint.idx == idx_datapoint).update(data_dict)

                # Commit the session
                database.commit(session, 1057)

                # Report success
                log_message = (
                    'Successful cache drain for UID %s at timestamp %s') % (
                        self.ingest.uid(), self.ingest.timestamp())
                log.log2quiet(1058, log_message)

    def _update_unchartable(self, mapping):
        """Update unchartable data into the database "iset_datapoint" table.

        Args:
            mapping: Map of DIDs to database row index values

        Returns:
            None

        """
        # Initialize key variables
        data = self.ingest.other()
        data_list = []
        timestamp_tracker = {}

        # Update data
        for item in data:
            # Process each datapoint item found
            (_, did, value, timestamp) = item
            idx_datapoint = int(mapping[did][0])
            last_timestamp = int(mapping[did][2])

            # Only update with data collected after
            # the most recent update. Don't do anything more
            if timestamp > last_timestamp:
                data_list.append(
                    (idx_datapoint, value)
                )

                # Update DID's last updated timestamp
                if idx_datapoint in timestamp_tracker:
                    timestamp_tracker[idx_datapoint] = max(
                        timestamp, timestamp_tracker[idx_datapoint])
                else:
                    timestamp_tracker[idx_datapoint] = timestamp

        # Update if there is data
        if bool(data_list) is True:
            # Create a database session
            # NOTE: We only do a single commit on the session.
            # This is much faster (20x based on testing) than
            # instantiating the database, updating records, and committing
            # after every iteration of the "for loop"
            database = db.Database()
            session = database.session()

            # Update uncharted data
            for item in data_list:
                (idx_datapoint, value) = item
                data_dict = {'uncharted_value': jm_general.encode(value)}
                session.query(Datapoint).filter(
                    Datapoint.idx == idx_datapoint).update(data_dict)

            # Change the last updated timestamp
            for idx_datapoint, last_timestamp in timestamp_tracker.items():
                data_dict = {'last_timestamp': last_timestamp}
                session.query(Datapoint).filter(
                    Datapoint.idx == idx_datapoint).update(data_dict)

            # Commit data
            database.commit(session, 1037)

            # Report success
            log_message = (
                'Successful cache drain (Uncharted Data) '
                'for UID %s at timestamp %s') % (
                    self.ingest.uid(), self.ingest.timestamp())
            log.log2quiet(1045, log_message)


def _insert_datapoint(metadata, idx_agent, idx_host):
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
        idx_agent: Index of agent in the Agent db table
        idx_host: Index of host in the Host db table

    Returns:
        None

    """
    # Initialize key variables
    (_, did, agent_label, agent_source, _, base_type) = metadata

    # Insert record
    record = Datapoint(
        id=jm_general.encode(did),
        idx_agent=idx_agent,
        idx_host=idx_host,
        agent_label=jm_general.encode(agent_label),
        agent_source=jm_general.encode(agent_source),
        base_type=base_type)
    database = db.Database()
    database.add(record, 1082)


def _datapoints_by_did(idx_agent):
    """Create dict of enabled datapoints and their corresponding indices.

    Args:
        idx_agent: Index of agent

    Returns:
        data: Dict keyed by datapoint ID,
            with a tuple as its value (idx, idx_agent)
            idx: Datapoint index
            idx_agent: Agent index
            last_timestamp: The last time the timestamp was updated

    """
    # Initialize key variables
    data = {}

    # Update database
    session = db.Database().session()
    result = session.query(
        Datapoint.id, Datapoint.idx,
        Datapoint.idx_agent, Datapoint.last_timestamp).filter(
            and_(Datapoint.enabled == 1, Datapoint.idx_agent == idx_agent))

    # Massage data
    for instance in result:
        did = instance.id.decode('utf-8')
        idx = instance.idx
        idx_agent = instance.idx_agent
        last_timestamp = instance.last_timestamp
        data[did] = (idx, idx_agent, last_timestamp)

    # Return the session to the database pool after processing
    session.close()

    # Return
    return data


def _host_agent_last_update(hostname, uid, last_timestamp):
    """Insert new datapoint into database.

    Args:
        uid: UID of agent
        last_timestamp: The last time a DID for the agent was updated
            in the database

    Returns:
        None

    """
    # Initialize key variables
    idx_agent = agent.GetUID(uid).idx()
    idx_host = dhost.GetHost(hostname).idx()

    # Update database
    database = db.Database()
    session = database.session()
    record = session.query(HostAgent).filter(
        and_(
            HostAgent.idx_host == idx_host,
            HostAgent.idx_agent == idx_agent)).one()
    record.last_timestamp = last_timestamp
    database.commit(session, 1124)


def _update_agent_last_update(uid, last_timestamp):
    """Insert new datapoint into database.

    Args:
        uid: UID of agent
        last_timestamp: The last time a DID for the agent was updated
            in the database

    Returns:
        None

    """
    # Initialize key variables
    value = jm_general.encode(uid)

    # Update the database
    database = db.Database()
    session = database.session()
    record = session.query(Agent).filter(Agent.id == value).one()
    record.last_timestamp = last_timestamp
    database.commit(session, 1055)


def validate_cache_files():
    """Method initializing the class.

    Args:
        agent_name: agent name

    Returns:
        None

    """
    # Initialize key variables
    uid_metadata = defaultdict(lambda: defaultdict(dict))

    # Configuration setup
    config = jm_configuration.Config()
    cache_dir = config.ingest_cache_directory()

    # Filenames must start with a numeric timestamp and #
    # end with a hex string. This will be tested later
    regex = re.compile(r'^\d+_[0-9a-f]+_[0-9a-f]+.json')

    # Add files in cache directory to list
    all_filenames = [filename for filename in os.listdir(
        cache_dir) if os.path.isfile(
            os.path.join(cache_dir, filename))]

    ######################################################################
    # Create threads
    ######################################################################

    # Process only valid agent filenames
    for filename in all_filenames:
        # Add valid data to lists
        if bool(regex.match(filename)) is True:
            # Create a complete filepath
            filepath = os.path.join(cache_dir, filename)

            # Only read files that are 15 seconds or older
            # to prevent corruption caused by reading a file that could be
            # updating simultaneously
            if time.time() - os.path.getmtime(filepath) < 15:
                continue

            # Create a dict of UIDs, timestamps and filepaths
            (name, _) = filename.split('.')
            (tstamp, uid, hosthash) = name.split('_')
            timestamp = int(tstamp)

            # Keep track of hosts and the UIDs that track them
            # Create a list of timestamp, host filepath tuples for each UID
            if bool(uid_metadata[hosthash][uid]) is True:
                uid_metadata[hosthash][uid].append((timestamp, filepath))
            else:
                uid_metadata[hosthash][uid] = [(timestamp, filepath)]

    # Return
    return uid_metadata


def process(agent_name):
    """Method initializing the class.

    Args:
        agent_name: agent name

    Returns:
        None

    """
    # Initialize key variables
    uid_metadata = defaultdict(lambda: defaultdict(dict))

    # Configuration setup
    config = jm_configuration.Config()
    threads_in_pool = config.ingest_threads()

    # Make sure we have database connectivity
    if db.connectivity() is False:
        log_message = (
            'No connectivity to database. Check if running. '
            'Check database authentication parameters.'
            '')
        log.log2warn(1053, log_message)
        return

    # Get meta data on files
    uid_metadata = validate_cache_files()

    # Spawn processes only if we have files to process
    if bool(uid_metadata.keys()) is True:
        # Process lock file
        f_obj = hidden.File()
        lockfile = f_obj.lock(agent_name)
        if os.path.exists(lockfile) is True:
            # Return if lock file is present
            log_message = (
                'Ingest lock file %s exists. Multiple ingest daemons running '
                'or lots of cache files to ingest. Ingester may have died '
                'catastrophically in the past, in which case the lockfile '
                'should be deleted. Exiting ingest process. '
                'Will try again later.'
                '') % (lockfile)
            log.log2warn(1069, log_message)
            return
        else:
            # Create lockfile
            open(lockfile, 'a').close()

        # Spawn a pool of threads, and pass them queue instance
        # Only create the required number of threads up to the
        # threads_in_pool maximum
        for _ in range(
                min(threads_in_pool, len(uid_metadata))):
            update_thread = ProcessUID(THREAD_QUEUE)
            update_thread.daemon = True

            # Sometimes we exhaust the thread abilities of the OS
            # even with the "threads_in_pool" limit. This is because
            # there could be a backlog of files to cache files process
            # and we have overlapping ingests due to a deleted lockfile.
            # This code ensures we don't exceed the limits.
            try:
                update_thread.start()
            except RuntimeError:
                log_message = (
                    'Too many threads created for cache ingest. '
                    'Verify that ingest lock file is present.')

                # Remove the lockfile so we can restart later then die
                os.remove(lockfile)
                log.log2die(1067, log_message)
            except:
                log_message = (
                    'Unknown error occurred when trying to '
                    'create cache ingest threads')

                # Remove the lockfile so we can restart later then die
                os.remove(lockfile)
                log.log2die(1072, log_message)

        # Read each cache file
        for hosthash in uid_metadata.keys():
            for uid in uid_metadata[hosthash].keys():
                ##############################################################
                #
                # Define variables that will be required for the threading
                # We have to initialize the dict during every loop to prevent
                # data corruption
                #
                ##############################################################
                data_dict = {}
                data_dict['uid'] = uid
                data_dict['metadata'] = uid_metadata[hosthash][uid]
                data_dict['config'] = config
                THREAD_QUEUE.put(data_dict)

        # Wait on the queue until everything has been processed
        THREAD_QUEUE.join()

        # PYTHON BUG. Join can occur while threads are still shutting down.
        # This can create spurious "Exception in thread (most likely raised
        # during interpreter shutdown)" errors.
        # The "time.sleep(1)" adds a delay to make sure things really terminate
        # properly. This seems to be an issue on virtual machines in Dev only
        time.sleep(1)

        # Return if lock file is present
        if os.path.exists(lockfile) is True:
            os.remove(lockfile)
