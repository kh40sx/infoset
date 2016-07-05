#!/usr/bin/env python3
"""infoset Sentry3 (Servertech intelligent CDU power strip) agent.

Description:

    Uses Python2 to be compatible with most Linux systems

    This script:
        1) Retrieves a variety of system information
        2) Posts the data using HTTP to a server listed
           in the configuration file

"""
# Standard libraries
import sys
import os
import json
from threading import Timer
import logging
from random import randint
import time
import hashlib
import argparse
import datetime
from collections import defaultdict

# pip3 libraries
import requests
import yaml

# infoset libraries
from infoset.utils import jm_configuration
from infoset.snmp import snmp_manager
from infoset.snmp import mib_sentry3

logging.getLogger('requests').setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG)


class Config(object):
    """Class gathers all configuration information.

    Args:
        None

    Returns:
        None

    Methods:
        __init__:
        https:
        port:
        server:
        descriptions:
    """

    def __init__(self, filename):
        """Function for intializing the class."""
        # Check if file exists
        if (os.path.isdir(filename) is True or
                os.path.exists(filename)) is False:
            log_message = (
                'Configuration file "%s" '
                'doesn\'t exist!' % filename)
            die(1002, log_message)

        # Cycle through list of files in directory
        if filename.endswith('.yaml'):
            # Read file and add to string
            with open(filename, 'r') as file_handle:
                data = file_handle.read()
        else:
            log_message = (
                'Configuration filename "%s" '
                'doesn\'t end with ".yaml"!' % filename)
            die(1003, log_message)

        # Return
        self.config_dict = yaml.load(data)

    def cache_dir(self):
        """Determine the cache_dir.

        Args:
            None

        Returns:
            value: configured cache_dir

        """
        # Get parameter
        value = self.config_dict['cache_dir']

        # Check if value exists
        if os.path.isdir(value) is False:
            log_message = (
                'cache_dir: "%s" '
                'in configuration doesn\'t exist!') % (value)
            die(1005, log_message)

        # Return
        return value

    def log_file(self):
        """Determine the log_file.

        Args:
            None

        Returns:
            value: configured log_file

        """
        # Get parameter
        value = self.config_dict['log_file']

        # Return
        return value

    def https(self):
        """Define whether the server is using HTTPS.

        Args:
            None

        Returns:
            value: https

        """
        # Get parameter
        if 'https' in self.config_dict:
            value = self.config_dict['https']
        else:
            value = False

        # Fix user errors
        if value is not False:
            value = True

        # Return
        return value

    def port(self):
        """Determine the TCP port the server is listening on.

        Args:
            None

        Returns:
            value: port

        """
        # Get parameter
        if 'port' in self.config_dict:
            result = self.config_dict['port']
        else:
            result = 5000

        # Port must be a number
        try:
            value = int(result)
        except:
            die(1000, '"port" in configuration file needs to be numeric')
        # Return
        return value

    def server(self):
        """Determine the server to receive the agent's data.

        Args:
            None

        Returns:
            value: server

        """
        # Get parameter
        value = self.config_dict['server']

        # Return
        return value

    def descriptions(self):
        """Determine the descriptions for each agent label.

        Args:
            None

        Returns:
            value: descriptions

        """
        # Get parameter
        value = self.config_dict['descriptions']

        # Return
        return value


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

    def __init__(self, uid, config):
        """Method initializing the class.

        Args:
            uid: Unique ID for Agent
            config: Configuration object

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
            die(1004, log_message)

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
            log(1007, log_message, self.config.log_file(), error=False)
        else:
            log_message = (
                'Failed to contact server %s'
                '') % (self.url)
            log(1008, log_message, self.config.log_file(), error=True)

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
                log(1009, log_message, self.config.log_file(), error=False)


def phone_home(uid, config, query):
    """Post system data to the central server.

    Args:
        uid: Unique ID for Agent
        config: Configuration object
        query: SNMP credentials object

    Returns:
        None

    """
    # Initialize key variables
    agent = Agent(uid, config)
    state = {}
    data = defaultdict(lambda: defaultdict(dict))
    labels = ['infeedPower', 'infeedLoadValue']
    prefix = 'Sentry3'

    # Get results from querying Servertech device
    state['infeedPower'] = _normalize_keys(query.infeedpower())
    state['infeedLoadValue'] = _normalize_keys(
        query.infeedloadvalue())
    state['infeedID'] = _normalize_keys(query.infeedid())

    # Create dictionary for eventual posting
    for label in labels:
        for key, value in state[label].items():
            source = state['infeedID'][key]
            data[label][source] = value

    # Populate agent
    agent.populate_dict(prefix, data)

    # Post data
    success = agent.post()

    # Purge cache if success is True
    if success is True:
        agent.purge()


def _normalize_keys(data, nodes=2):
    """Normalize SNMP results.

    Args:
        data: Dict of results
        nodes: Last number of nodes in OID to use as a key

    Returns:
        result: Dict with new key

    """
    # Initialize key variables
    intermediate = {}
    result = {}
    count = 0

    # Iterate
    for key, value in data.items():
        nodes = key.split('.')
        new_key = ('%s.%s') % (nodes[-2], nodes[-1])
        intermediate[new_key] = value

    # Do again but convert to numeric keys
    for _, value in sorted(intermediate.items()):
        result[count] = value
        count += 1

    # Return
    return result


def log(code, message, filename, error=True):
    """Log message to file.

    Args:
        code: Message code
        message: Message text
        filename: Log filename
        error: If True, create a different message string

    Returns:
        None

    """
    # Initialize key variables
    output = _message(code, message, error)

    # Write to file
    with open(filename, 'a') as f_handle:
        f_handle.write(
            ('%s\n') % (output)
        )


def _message(code, message, error=True):
    """Create a formatted message string.

    Args:
        code: Message code
        message: Message text
        error: If True, create a different message string

    Returns:
        output: Message result

    """
    # Initialize key variables
    time_object = datetime.datetime.fromtimestamp(time.time())
    timestring = time_object.strftime('%Y-%m-%d %H:%M:%S,%f')

    # Format string for error message, print and die
    if error is True:
        prefix = 'ERROR'
    else:
        prefix = 'STATUS'
    output = ('%s - %s - [%s] (%s)') % (timestring, prefix, code, message)

    # Return
    return output


def die(code, message):
    """Print error message and die.

    Args:
        code: Error code
        message: Error message to print to screen

    Returns:
        None

    """
    # Initialize key variables
    output = _message(code, message)

    # Format string for error message, print and die
    print(output)
    sys.exit(2)


def create_environment(hostname):
    """Create a permanent UID for the agent.

    Args:
        hostname: Host to create UID for

    Returns:
        uid: UID for agent

    """
    # Initialize key variables
    home_dir = os.environ['HOME']
    uid_dir = ('%s/.infoset/uid') % (home_dir)
    filename = ('%s/%s') % (uid_dir, hostname)

    # Create UID directory if not yet created
    if os.path.exists(uid_dir) is False:
        os.makedirs(uid_dir)

    # Read environment file with UID if it exists
    if os.path.isfile(filename):
        with open(filename) as f_handle:
            uid = f_handle.readline()
    else:
        # Create a UID and save
        prehash = ('%s%s') % (randint(0, 50), time.time())
        hasher = hashlib.sha256()
        hasher.update(bytes(prehash.encode()))
        uid = hasher.hexdigest()

        # Save UID
        with open(filename, 'w+') as env:
            env.write(str(uid))

    # Return
    return uid


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
        '--config_file',
        dest='config_file',
        required=True,
        default=None,
        type=str,
        help='Config file to use.'
    )

    # CLI argument for the auth directory
    parser.add_argument(
        '--auth_dir',
        dest='auth_dir',
        required=True,
        default=None,
        type=str,
        help='Authentication directory to use.'
    )

    # CLI argument for the host to poll
    parser.add_argument(
        '--hostname',
        dest='hostname',
        required=True,
        default=None,
        type=str,
        help='Host to poll.'
    )

    # Return the CLI arguments
    args = parser.parse_args()

    # Return our parsed CLI arguments
    return args


def main():
    """Start the infoset agent.

    Args:
        None

    Returns:
        None

    """
    # Get configuration
    args = process_cli()
    config = Config(args.config_file)

    # Get snmp configuration information from infoset
    iconfig = jm_configuration.ConfigReader(args.auth_dir)
    validate = snmp_manager.Validate(args.hostname, iconfig.snmp_auth())
    snmp_params = validate.credentials()
    if snmp_params is None:
        log_message = (
            'No valid SNMP configuration found '
            'for host "%s" ') % (args.hostname)
        die(1006, log_message)

    # Create Query make sure MIB is supported
    snmp_object = snmp_manager.Interact(snmp_params)
    query = mib_sentry3.init_query(snmp_object)
    if query.supported() is False:
        log_message = (
            'The Sentry3 MIB is not supported by host  "%s"'
            '') % (args.hostname)
        die(1001, log_message)

    # Get the UID for the agent after all preliminary checks are OK
    uid_env = create_environment(args.hostname)

    # Post data to the remote server
    phone_home(uid_env, config, query)

    # Do the daemon thing
    Timer(10, main).start()


if __name__ == "__main__":
    main()
