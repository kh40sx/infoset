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

# pip3 libraries
import requests

# infoset libraries
from infoset.utils import hidden
from infoset.utils import Daemon
from infoset.utils import log
from infoset.utils import jm_general
from infoset.language import language


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

    def __init__(self, uid, config, hostname):
        """Method initializing the class.

        Args:
            uid: Unique ID for Agent
            config: ConfigAgent configuration object
            agent_name: Name of agent
            hostname: Hostname that the agent applies to

        Returns:
            None

        """
        # Initialize key variables
        self.data = defaultdict(lambda: defaultdict(dict))
        self.config = config
        self.timestamp = jm_general.normalized_timestamp()

        # Add timestamp
        self.data['timestamp'] = self.timestamp
        self.data['uid'] = uid
        self.data['agent'] = config.agent_name()
        self.data['hostname'] = hostname

        # Construct URL for server
        if config.server_https() is True:
            prefix = 'https://'
        else:
            prefix = 'http://'
        self.url = (
            '%s%s:%s/receive/%s') % (
                prefix, self.config.server_name(),
                self.config.server_port(), uid)

        # Create the cache directory
        self.cache_dir = self.config.agent_cache_directory()
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

    def populate(self, label, data, base_type='floating', chartable=False):
        """Populate data for agent to eventually send to server.

        Args:
            label: label to use for data
            data: List of data tuples [(value, source)]
                where source is the subsystem name generating the data. This
                data will be converted to a tuple list if it is a single value.
            base_type: SNMP style base type (integer, counter32, counter64)
            chartable: Chartable data if True

        Returns:
            None

        """
        # Initialize key variables
        agent_name = self.name()
        output = {}
        value_tuples = []
        index = 0
        base_types = [None, 'counter32', 'counter64', 'floating']

        # Validate base_type
        if base_type not in base_types:
            log_message = (
                'base_type %s is unsupported for label "%s"'
                '') % (base_type, label)
            log.log2die(1025, log_message)

        # Convert data to list of tuples if required
        if isinstance(data, list) is False:
            value_sources = [(data, None)]
        else:
            value_sources = data

        # Get a description to use for label value
        lang = language.Agent(agent_name)
        description = lang.label_description(label)

        #####################################################################
        # This section fills self.data with lists of tuples keyed by "label"
        #
        # Each tuple list has the following structure:
        #
        # 0) Index value
        # 1) Value of data
        # 2) Source of data (eg. Interface name)
        #
        #####################################################################

        # Populate tuple list
        for value_source in value_sources:
            value = value_source[0]
            source = value_source[1]
            value_tuples.append(
                (index, value, source)
            )
            index += 1

        # Add base_type and a description to the data to be returned
        output['description'] = description
        output['base_type'] = base_type
        output['data'] = value_tuples

        # Add a key if chartable
        if chartable is True:
            self.data['chartable'][label] = output
        else:
            self.data['other'][label] = output

    def populate_dict(self, prefix, data, base_type='floating'):
        """Populate agent with data that's a dict keyed by [label][source].

        Args:
            prefix: Prefix to append to data keys when populating the agent
            data: Dict of data to post keyed, by [label][source]
            base_type: SNMP style base_type (integer, counter32, etc.)

        Returns:
            None

        """
        # Iterate over labels
        for label in data.keys():
            # Initialize tuple list to use by agent.populate
            value_sources = []

            # Append to tuple list
            # (Sorting is important to keep consistent ordering)
            for source, value in sorted(data[label].items()):
                value_sources.append(
                    (value, source)
                )

            # Update agent
            new_label = ('%s_%s') % (prefix, label)
            self.populate(
                new_label, value_sources, chartable=True, base_type=base_type)

    def populate_named_tuple(self, prefix, data, base_type='floating'):
        """Post system data to the central server.

        Args:
            agent: agent object
            data: Named tuple with data values
            prefix: Prefix to append to data keys when populating the agent
            base_type: SNMP style base_type (integer, counter32, etc.)

        Returns:
            None

        """
        # Initialize key variables
        source = None

        # Get data
        system_dict = data._asdict()
        for label, value in system_dict.items():
            # Convert the dict to two dimensional dict keyed by [label][source]
            # for use by self.populate_dict
            multikey = defaultdict(lambda: defaultdict(dict))
            multikey[label][source] = value

            # Update agent
            self.populate_dict(prefix, multikey, base_type=base_type)

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
                    json.dump(self.data, f_handle)

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
                data = json.load(f_handle)

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
        self.pidfile = f_obj.pid(agent_name)

        # Call up the base daemon
        Daemon.__init__(self, self.pidfile)

    def run(self):
        """Start polling.

        Args:
            None

        Returns:
            None

        """
        # Start polling
        while True:
            time.sleep(1)
            self.poller.query()
            time.sleep(299)


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


def get_uid(hostname):
    """Create a permanent UID for the agent.

    Args:
        hostname: Host to create UID for

    Returns:
        uid: UID for agent

    """
    # Initialize key variables
    filez = hidden.File()
    dirz = hidden.Directory()
    uid_dir = dirz.uid()
    filename = filez.uid(hostname)

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
