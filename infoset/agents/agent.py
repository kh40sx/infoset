#!/usr/bin/env python2
"""infoset Agent class.

Description:

    Uses Python2 to be compatible with most Linux systems

    This script:
        1) Processes a variety of information from agents
        2) Posts the data using HTTP to a server listed
           in the configuration file

"""
# Standard libraries
import sys
import os
import json
import logging
import time
from collections import defaultdict

# pip3 libraries
import requests

# infoset libraries
from infoset.utils import jm_general

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

    def __init__(self, uid, config, agent_name):
        """Method initializing the class.

        Args:
            uid: Unique ID for Agent
            config: Configuration object
            agent_name: Name of agent

        Returns:
            None

        """
        # Initialize key variables
        self.data = defaultdict(lambda: defaultdict(dict))
        self.config = config
        self.timestamp = (int(time.time()) // 300) * 300

        # Add timestamp
        self.data['timestamp'] = self.timestamp
        self.data['uid'] = uid
        self.data['agent'] = agent_name

        # Construct URL for server
        if config.https() is True:
            prefix = 'https://'
        else:
            prefix = 'http://'
        self.url = (
            '%s%s:%s/receive/%s') % (
                prefix, self.config.server(),
                self.config.port(), uid)

        # Create the cache directory
        self.cache_dir = ('%s/infoset_cache') % (self.config.cache_dir())
        if os.path.exists(self.cache_dir) is False:
            os.mkdir(self.cache_dir)

    def populate(self, label, data, base_type='gauge', chartable=False):
        """Populate data for agent to eventually send to server.

        Args:
            label: label to use for data
            data: List of data tuples [(value, source)]
                where source is the subsystem name generating the data. This
                data will be converted to a tuple list if it is a single value.
            base_type: SNMP style base type (gauge, counter32, counter64)
            chartable: Chartable data if True

        Returns:
            None

        """
        # Initialize key variables
        descriptions = self.config.descriptions()
        output = {}
        value_tuples = []
        index = 0
        base_types = [None, 'counter32', 'counter64', 'gauge']

        # Validate base_type
        if base_type not in base_types:
            log_message = (
                'base_type %s is unsupported for label "%s"'
                '') % (base_type, label)
            jm_general.logit(1004, log_message)

        # Convert data to list of tuples if required
        if isinstance(data, list) is False:
            value_sources = [(data, None)]
        else:
            value_sources = data

        # Get a description to use for label value
        if label in descriptions:
            description = descriptions[label]
        else:
            description = None

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

    def populate_dict(self, prefix, data, base_type='gauge'):
        """Populate agent with data that's a dict keyed by [label][source].

        Args:
            prefix: Prefix to append to data keys when populating the agent
            data: Dict of data to post keyed, by [label][source]
            base_type: SNMP style base_type (gauge, counter32, etc.)

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

    def populate_named_tuple(self, prefix, data, base_type='gauge'):
        """Post system data to the central server.

        Args:
            agent: agent object
            data: Named tuple with data values
            prefix: Prefix to append to data keys when populating the agent
            base_type: SNMP style base_type (gauge, counter32, etc.)

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

        # Create data to post
        if data is None:
            data = self.data

        # Post data save to cache if this fails
        try:
            result = requests.post(self.url, json=data)
            response = True
        except:
            if save is True:
                filename = ('%s/%s.json') % (self.cache_dir, self.timestamp)
                with open(filename, 'w') as f_handle:
                    json.dump(self.data, f_handle)

        # Define success
        if response is True:
            if result.status_code == 200:
                success = True

        # Log message
        if success is True:
            log_message = (
                'Successfully contacted server %s'
                '') % (self.url)
            jm_general.log(1007, log_message, self.config.log_file())
        else:
            log_message = (
                'Failed to contact server %s'
                '') % (self.url)
            jm_general.log(
                1008, log_message, self.config.log_file())

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
                jm_general.log(1009, log_message, self.config.log_file())
