#!/usr/bin/env python3
"""infoset Sentry3 (Servertech intelligent CDU power strip) agent.

Description:

    This script:
        1) Retrieves a variety of system information
        2) Posts the data using HTTP to a server listed
           in the configuration file

"""
# Standard libraries
from threading import Timer
import logging
import argparse
from collections import defaultdict

# infoset libraries
from infoset.agents import agent as Agent
from infoset.utils import jm_configuration
from infoset.utils import jm_general
from infoset.snmp import snmp_manager
from infoset.snmp import mib_if
from infoset.snmp import mib_if_64

logging.getLogger('requests').setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG)


class PollingAgent(object):
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

    def __init__(self, config_dir):
        """Method initializing the class.

        Args:
            config_dir: Configuration directory

        Returns:
            None

        """
        # Initialize key variables
        agent_name = 'interfaces'

        # Get configuration
        self.config = jm_configuration.ConfigAgent(config_dir, agent_name)

        # Get snmp configuration information from infoset
        self.snmp_config = jm_configuration.ConfigSNMP(config_dir)

    def query(self):
        """Query all remote hosts for data.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        log_file = self.config.log_file()

        # Check each hostname
        hostnames = self.config.agent_snmp_hostnames()
        for hostname in hostnames:
            # Get valid SNMP credentials
            validate = snmp_manager.Validate(
                hostname, self.snmp_config.snmp_auth())
            snmp_params = validate.credentials()

            # Log message
            if snmp_params is None:
                log_message = (
                    'No valid SNMP configuration found '
                    'for host "%s" ') % (hostname)
                jm_general.log(1022, log_message, log_file, error=False)
                continue

            # Create Query make sure MIB is supported
            snmp_object = snmp_manager.Interact(snmp_params)
            query = mib_if.init_query(snmp_object)
            query64 = mib_if_64.init_query(snmp_object)
            if query.supported() is False:
                log_message = (
                    'The IF-MIB is not supported by host  "%s"'
                    '') % (hostname)
                jm_general.log(1024, log_message, log_file, error=False)
                continue

            # Get the UID for the agent after all preliminary checks are OK
            uid_env = Agent.get_uid(hostname)

            # Post data to the remote server
            self.upload(uid_env, hostname, query, query64)

        # Do the daemon thing
        Timer(300, main).start()

    def upload(self, uid, hostname, query, query64):
        """Post system data to the central server.

        Args:
            uid: Unique ID for Agent
            hostname: Hostname
            query: SNMP credentials object (IF-MIB 32 bit)
            query64: SNMP credentials object (IF-MIB 64 bit)

        Returns:
            None

        """
        # Initialize key variables
        ignore = []
        agent = Agent.Agent(uid, self.config, hostname)

        # Get a list of interfaces to ignore because they are down
        status = query.ifoperstatus()
        for key, value in status.items():
            if value != 1:
                ignore.append(key)

        # Update 32 bit data
        _update_32(agent, ignore, query)

        # Update 64 bit data
        _update_64(agent, ignore, query, query64)

        # Post data
        success = agent.post()

        # Purge cache if success is True
        if success is True:
            agent.purge()


def _update_64(agent, ignore, query, query64):
    """Return all the CLI options.

    Args:
        agent: Agent object
        ignore: List of ifIndexes to ignore
        query: SNMP query object
        query64: SNMP query object (64 bit)

    Returns:
        None

    """
    # Initialize key variables
    prefix = ''
    state = {}
    data = defaultdict(lambda: defaultdict(dict))

    # Don't provide 64 bit counter data if not supported
    if query64.supported() is False:
        return

    ##########################################################################
    # Handle 64 bit counters
    ##########################################################################
    labels = ['ifHCInOctets', 'ifHCOutOctets']
    state['ifHCInOctets'] = query64.ifhcinoctets()
    state['ifHCOutOctets'] = query64.ifhcoutoctets()
    state['ifDescr'] = query.ifdescr()

    # Create dictionary for eventual posting
    for label in labels:
        for key, value in state[label].items():
            if key in ignore:
                continue
            source = state['ifDescr'][key]
            data[label][source] = value * 8

    # Populate agent
    agent.populate_dict(prefix, data, base_type='counter64')


def _update_32(agent, ignore, query):
    """Return all the CLI options.

    Args:
        agent: Agent object
        ignore: List of ifIndexes to ignore
        query: SNMP query object

    Returns:
        None

    """
    # Initialize key variables
    prefix = ''
    state = {}
    data = defaultdict(lambda: defaultdict(dict))

    ##########################################################################
    # Handle 32 bit counters
    ##########################################################################
    # Get results from querying device
    labels = ['ifInOctets', 'ifOutOctets']
    state['ifInOctets'] = query.ifinoctets()
    state['ifOutOctets'] = query.ifoutoctets()
    state['ifDescr'] = query.ifdescr()

    # Create dictionary for eventual posting
    for label in labels:
        for key, value in state[label].items():
            if key in ignore:
                continue
            source = state['ifDescr'][key]
            data[label][source] = value * 8

    # Populate agent
    agent.populate_dict(prefix, data, base_type='counter32')


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

    # CLI argument for the auth directory
    parser.add_argument(
        '--config_dir',
        dest='config_dir',
        required=True,
        default=None,
        type=str,
        help='Configuration directory to use.'
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

    # Instantiate and poll
    poller = PollingAgent(args.config_dir)
    poller.query()


if __name__ == "__main__":
    main()
