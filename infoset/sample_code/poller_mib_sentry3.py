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
import os
from threading import Timer
import logging
import argparse
from collections import defaultdict

# pip3 libraries
import yaml

# infoset libraries
from infoset.agents import agent
from infoset.utils import jm_configuration
from infoset.utils import jm_general
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
            jm_general.die(1002, log_message)

        # Cycle through list of files in directory
        if filename.endswith('.yaml'):
            # Read file and add to string
            with open(filename, 'r') as file_handle:
                data = file_handle.read()
        else:
            log_message = (
                'Configuration filename "%s" '
                'doesn\'t end with ".yaml"!' % filename)
            jm_general.die(1003, log_message)

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
            jm_general.die(1005, log_message)

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
            jm_general.die(
                1000, '"port" in configuration file needs to be numeric')
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
    agent_obj = agent.Agent(uid, config, 'Sentry3')
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
    agent_obj.populate_dict(prefix, data)

    # Post data
    success = agent_obj.post()

    # Purge cache if success is True
    if success is True:
        agent_obj.purge()


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
        jm_general.die(1006, log_message)

    # Create Query make sure MIB is supported
    snmp_object = snmp_manager.Interact(snmp_params)
    query = mib_sentry3.init_query(snmp_object)
    if query.supported() is False:
        log_message = (
            'The Sentry3 MIB is not supported by host  "%s"'
            '') % (args.hostname)
        jm_general.die(1001, log_message)

    # Get the UID for the agent after all preliminary checks are OK
    uid_env = agent.get_uid(args.hostname)

    # Post data to the remote server
    phone_home(uid_env, config, query)

    # Do the daemon thing
    Timer(10, main).start()


if __name__ == "__main__":
    main()
