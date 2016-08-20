#!/usr/bin/env python3
"""infoset Agent class.

Description:

    This script:
        1) Processes a variety of information from agents
        2) Posts the data using HTTP to a server listed
           in the configuration file

"""
# Standard libraries
import os
import sys
import json
import logging
import time
from collections import defaultdict
from random import random
import argparse
import queue as Queue
import threading
from copy import deepcopy

# pip3 libraries
import requests

# infoset libraries
from infoset.utils import hidden
from infoset.utils import Daemon
from infoset.utils import log
from infoset.utils import jm_general
from infoset.utils import jm_configuration
from infoset.language import language

# Define a key global variable
THREAD_QUEUE = Queue.Queue()

logging.getLogger('requests').setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG)


class Agent(object):
    """Infoset agent that gathers data.

    Args:
        None

    Returns:
        None

    Functions:
        __init__:
        populate:
        post:
    """

    def __init__(self, config, hostname):
        """Method initializing the class.

        Args:
            config: ConfigAgent configuration object
            agent_name: Name of agent
            hostname: Hostname that the agent applies to

        Returns:
            None

        """
        # Initialize key variables
        self.data = defaultdict(lambda: defaultdict(dict))
        agent_name = config.agent_name()
        uid = _get_uid(agent_name)
        self.lang = language.Agent(agent_name)

        # Add timestamp
        self.data['timestamp'] = jm_general.normalized_timestamp()
        self.data['uid'] = uid
        self.data['agent'] = agent_name
        self.data['hostname'] = hostname

        # Construct URL for server
        if config.server_https() is True:
            prefix = 'https://'
        else:
            prefix = 'http://'
        self.url = (
            '%s%s:%s/receive/%s') % (
                prefix, config.server_name(),
                config.server_port(), uid)

        # Create the cache directory
        self.cache_dir = config.agent_cache_directory()
        if os.path.exists(self.cache_dir) is False:
            os.mkdir(self.cache_dir)

    def name(self):
        """Return the name of the agent.

        Args:
            None

        Returns:
            value: Name of agent

        """
        # Return
        value = self.data['agent']
        return value

    def populate(self, data_in):
        """Populate data for agent to eventually send to server.

        Args:
            data_in: dict of datapoint values from agent
            chartable: Chartable data if True

        Returns:
            None

        """
        # Initialize data
        data = deepcopy(data_in)

        # Validate base_type
        if len(data) != 1 or isinstance(data, defaultdict) is False:
            log_message = ('Agent data "%s" is invalid') % (data)
            log.log2die(1025, log_message)

        # Get a description to use for label value
        for label in data.keys():
            description = self.lang.label_description(label)
            data['description'] = description
            break

        # Add data to appropriate self.data key
        if data[label]['base_type'] is not None:
            self.data['chartable'].update(data)
        else:
            self.data['other'].update(data)

    def populate_single(self, label, value, base_type=None, source=None):
        """Populate a single value in the agent.

        Args:
            label: Agent label for data
            value: Value of data
            source: Source of the data
            base_type: Base type of data

        Returns:
            None

        """
        # Initialize key variables
        data = defaultdict(lambda: defaultdict(dict))
        data[label]['base_type'] = base_type
        data[label]['data'] = [[0, value, source]]

        # Update
        self.populate(data)

    def populate_named_tuple(self, named_tuple, prefix='', base_type=1):
        """Post system data to the central server.

        Args:
            named_tuple: Named tuple with data values
            prefix: Prefix to append to data keys when populating the agent
            base_type: SNMP style base_type (integer, counter32, etc.)

        Returns:
            None

        """
        # Get data
        system_dict = named_tuple._asdict()
        for label, value in system_dict.items():
            # Convert the dict to two dimensional dict keyed by [label][source]
            # for use by self.populate_dict
            new_label = ('%s_%s') % (prefix, label)

            # Initialize data
            data = defaultdict(lambda: defaultdict(dict))

            # Add data
            data[new_label]['data'] = [[0, value, None]]
            data[new_label]['base_type'] = base_type

            # Update
            self.populate(data)

    def populate_dict(self, data_in, prefix='', base_type=1):
        """Populate agent with data that's a dict keyed by [label][source].

        Args:
            data_in: Dict of data to post "X[label][source] = value"
            prefix: Prefix to append to data keys when populating the agent
            base_type: SNMP style base_type (integer, counter32, etc.)

        Returns:
            None

        """
        # Initialize data
        data_input = deepcopy(data_in)

        # Iterate over labels
        for label in data_input.keys():
            # Initialize tuple list to use by agent.populate
            value_sources = []
            new_label = ('%s_%s') % (prefix, label)

            # Initialize data
            data = defaultdict(lambda: defaultdict(dict))
            data[new_label]['base_type'] = base_type

            # Append to tuple list
            # (Sorting is important to keep consistent ordering)
            for source, value in sorted(data_input[label].items()):
                value_sources.append(
                    [source, value, source]
                )
            data[new_label]['data'] = value_sources

            # Update
            self.populate(data)

    def polled_data(self):
        """Return that that should be posted.

        Args:
            None

        Returns:
            None

        """
        # Return
        return self.data

    def post(self, save=True, data=None):
        """Post data to central server.

        Args:
            save: When True, save data to cache directory if postinf fails
            data: Data to post. If None, then uses self.data

        Returns:
            success: "True: if successful

        """
        # Initialize key variables
        success = False
        response = False
        timestamp = self.data['timestamp']
        uid = self.data['uid']

        # Create data to post
        if data is None:
            data = self.data

        # Post data save to cache if this fails
        try:
            result = requests.post(self.url, json=data)
            response = True
        except:
            if save is True:
                # Create a unique very long filename to reduce risk of
                hosthash = jm_general.hashstring(self.data['hostname'], sha=1)
                filename = ('%s/%s_%s_%s.json') % (
                    self.cache_dir, timestamp, uid, hosthash)

                # Save data
                with open(filename, 'w') as f_handle:
                    json.dump(data, f_handle)

        # Define success
        if response is True:
            if result.status_code == 200:
                success = True

        # Log message
        if success is True:
            log_message = (
                'Agent "%s" successfully contacted server %s'
                '') % (self.name(), self.url)
            log.log2quiet(1027, log_message)
        else:
            log_message = (
                'Agent "%s" failed to contact server %s'
                '') % (self.name(), self.url)
            log.log2warn(1028, log_message)

        # Return
        return success

    def purge(self):
        """Purge data from cache by posting to central server.

        Args:
            None

        Returns:
            success: "True: if successful

        """
        # Add files in cache directory to list
        filenames = [filename for filename in os.listdir(
            self.cache_dir) if os.path.isfile(
                os.path.join(self.cache_dir, filename))]

        # Read cache file
        for filename in filenames:
            filepath = os.path.join(self.cache_dir, filename)
            with open(filepath, 'r') as f_handle:
                try:
                    data = json.load(f_handle)
                except:
                    # Log removal
                    log_message = (
                        'Error reading previously cached agent data file %s '
                        'for agent %s. May be corrupted.'
                        '') % (filepath, self.name())
                    log.log2die(1064, log_message)

            # Post file
            success = self.post(save=False, data=data)

            # Delete file if successful
            if success is True:
                os.remove(filepath)

                # Log removal
                log_message = (
                    'Purging cache file %s after successfully '
                    'contacting server %s'
                    '') % (filepath, self.url)
                log.log2quiet(1029, log_message)


class AgentDaemon(Daemon):
    """Class that manages polling.

    Args:
        None

    Returns:
        None

    """

    def __init__(self, poller):
        """Method initializing the class.

        Args:
            poller: PollingAgent object

        Returns:
            None

        """
        # Instantiate poller
        self.poller = poller

        # Get PID filename
        agent_name = self.poller.name()
        f_obj = hidden.File()
        pidfile = f_obj.pid(agent_name)
        lockfile = f_obj.lock(agent_name)

        # Call up the base daemon
        Daemon.__init__(self, pidfile, lockfile=lockfile)

    def run(self):
        """Start polling.

        Args:
            None

        Returns:
            None

        """
        # Start polling. (Poller decides frequency)
        while True:
            self.poller.query()


class AgentCLI(object):
    """Class that manages the agent CLI.

    Args:
        None

    Returns:
        None

    """

    def __init__(self):
        """Method initializing the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        self.parser = None

        # Check environment
        log.check_environment()
        self.config_directory = os.environ['INFOSET_CONFIGDIR']

    def config_dir(self):
        """Return configuration directory.

        Args:
            None

        Returns:
            value: Configuration directory

        """
        # Return
        value = self.config_directory
        return value

    def process(self, additional_help=None):
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

        # CLI argument for stopping
        parser.add_argument(
            '--stop',
            required=False,
            default=False,
            action='store_true',
            help='Stop the agent daemon.'
        )

        # CLI argument for starting
        parser.add_argument(
            '--start',
            required=False,
            default=False,
            action='store_true',
            help='Start the agent daemon.'
        )

        # CLI argument for starting
        parser.add_argument(
            '--status',
            required=False,
            default=False,
            action='store_true',
            help='Get daemon daemon status.'
        )

        # CLI argument for restarting
        parser.add_argument(
            '--restart',
            required=False,
            default=False,
            action='store_true',
            help='Restart the agent daemon.'
        )

        # Get the parser value
        self.parser = parser

    def control(self, poller):
        """Start the infoset agent.

        Args:
            poller: PollingAgent object

        Returns:
            None

        """
        # Get the CLI arguments
        self.process()
        parser = self.parser
        args = parser.parse_args()

        # Run daemon
        daemon = AgentDaemon(poller)
        if args.start is True:
            daemon.start()
        elif args.stop is True:
            daemon.stop()
        elif args.restart is True:
            daemon.restart()
        elif args.status is True:
            daemon.status()
        else:
            parser.print_help()
            sys.exit(2)


class AgentThread(threading.Thread):
    """Threaded ingestion of agent files.

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
            poller = self.queue.get()
            poller.query()

            # All done!
            self.queue.task_done()


def _get_uid(agent_name):
    """Create a permanent UID for the agent.

    Args:
        agent_name: Agent to create UID for

    Returns:
        uid: UID for agent

    """
    # Initialize key variables
    filez = hidden.File()
    dirz = hidden.Directory()
    uid_dir = dirz.uid()
    filename = filez.uid(agent_name)

    # Create UID directory if not yet created
    if os.path.exists(uid_dir) is False:
        os.makedirs(uid_dir)

    # Read environment file with UID if it exists
    if os.path.isfile(filename):
        with open(filename) as f_handle:
            uid = f_handle.readline()
    else:
        # Create a UID and save
        prehash = ('%s%s%s%s%s') % (
            random(), random(), random(), random(), time.time())
        uid = jm_general.hashstring(prehash)

        # Save UID
        with open(filename, 'w+') as env:
            env.write(str(uid))

    # Return
    return uid


def threads(agent_name, pollers):
    """Function where agents poll devices using multithreading.

    Args:
        agent_name: Agent name
        pollers: List of polling objects

    Returns:
        None

    """
    # Get configuration
    config_dir = os.environ['INFOSET_CONFIGDIR']
    config = jm_configuration.ConfigServer(config_dir)
    threads_in_pool = config.agent_threads()

    # Spawn processes only if we have files to process
    if bool(pollers) is True:
        # Process lock file
        f_obj = hidden.File()
        lockfile = f_obj.lock(agent_name)
        if os.path.exists(lockfile) is True:
            # Return if lock file is present
            log_message = (
                'Agent lock file %s exists. Multiple agent daemons '
                'running or the daemon may have died '
                'catastrophically in the past, in which case the lockfile '
                'should be deleted. Exiting agent process. '
                'Will try again later.'
                '') % (lockfile)
            log.log2warn(1044, log_message)
            return
        else:
            # Create lockfile
            open(lockfile, 'a').close()

        # Spawn a pool of threads, and pass them queue instance
        for _ in range(
                min(threads_in_pool, len(pollers))):
            update_thread = AgentThread(THREAD_QUEUE)
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
                    'Too many threads created for agent "%s". '
                    'Verify that agent lock file is present.') % (agent_name)

                # Remove the lockfile so we can restart later then die
                os.remove(lockfile)
                log.log2die(1078, log_message)
            except:
                log_message = (
                    'Unknown error occurred when trying to '
                    'create threads for agent "%s"') % (agent_name)

                # Remove the lockfile so we can restart later then die
                os.remove(lockfile)
                log.log2die(1079, log_message)

        # Start polling
        for poller in pollers:
            ##############################################################
            #
            # Define variables that will be required for the threading
            # We have to initialize the dict during every loop to prevent
            # data corruption
            #
            ##############################################################
            THREAD_QUEUE.put(poller)

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
