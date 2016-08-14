#!/usr/bin/env python3
"""infoset Sentry3 (Servertech intelligent CDU power strip) agent.

Description:

    This script:
        1) Retrieves a variety of system information
        2) Posts the data using HTTP to a server listed
           in the configuration file

"""
# Standard libraries
import sys
import os
import logging
from collections import defaultdict
from time import sleep

# infoset libraries
try:
    from infoset.agents import agent as Agent
except:
    print('You need to set your PYTHONPATH to include the infoset library')
    sys.exit(2)
from infoset.utils import jm_configuration
from infoset.snmp import snmp_manager
from infoset.snmp import mib_sentry3
from infoset.utils import log

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

    def __init__(self):
        """Method initializing the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        self.agent_name = 'sentry3'

        # Get configuration
        config_dir = os.environ['INFOSET_CONFIGDIR']
        self.config = jm_configuration.ConfigAgent(
            config_dir, self.agent_name)

        # Get snmp configuration information from infoset
        self.snmp_config = jm_configuration.ConfigSNMP(config_dir)

    def name(self):
        """Return agent name.

        Args:
            None

        Returns:
            value: Name of agent

        """
        # Return
        value = self.agent_name
        return value

    def query(self):
        """Query all remote hosts for data.

        Args:
            None

        Returns:
            None

        """
        # Post data to the remote server
        while True:
            self._poll()

            # Sleep
            sleep(300)

    def _poll(self):
        """Query all remote hosts for data.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        pollers = []

        # Check each hostname
        hostnames = self.config.agent_hostnames()
        for hostname in hostnames:
            poller = Poller(hostname, self.agent_name)
            pollers.append(poller)

        # Start threaded polling
        if bool(pollers) is True:
            Agent.threads(self.agent_name, pollers)


class Poller(object):
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

    def __init__(self, hostname, agent_name):
        """Method initializing the class.

        Args:
            hostname: Hostname to poll
            agent_name: Name of agent

        Returns:
            None

        """
        # Initialize key variables
        self.agent_name = agent_name
        self.hostname = hostname

        # Get configuration
        config_dir = os.environ['INFOSET_CONFIGDIR']
        self.config = jm_configuration.ConfigAgent(
            config_dir, self.agent_name)

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
        hostname = self.hostname

        # Get valid SNMP credentials
        validate = snmp_manager.Validate(
            hostname, self.snmp_config.snmp_auth())
        snmp_params = validate.credentials()

        # Log message
        if snmp_params is None:
            log_message = (
                'No valid SNMP configuration found '
                'for host "%s" ') % (hostname)
            log.log2warn(1006, log_message)
            return

        # Create Query make sure MIB is supported
        snmp_object = snmp_manager.Interact(snmp_params)
        snmp_query = mib_sentry3.init_query(snmp_object)
        if snmp_query.supported() is False:
            log_message = (
                'The Sentry3 MIB is not supported by host  "%s"'
                '') % (hostname)
            log.log2warn(1001, log_message)
            return

        # Post data to the remote server
        self.upload(snmp_query)

    def upload(self, query):
        """Post system data to the central server.

        Args:
            query: SNMP credentials object

        Returns:
            None

        """
        # Initialize key variables
        hostname = self.hostname
        agent_obj = Agent.Agent(self.config, hostname)
        state = {}
        data = defaultdict(lambda: defaultdict(dict))
        labels = ['infeedPower', 'infeedLoadValue']
        prefix = 'Sentry3'

        # Get results from querying Servertech device
        state['infeedPower'] = _normalize_keys(query.infeedpower(safe=True))
        state['infeedLoadValue'] = _normalize_keys(
            query.infeedloadvalue(safe=True))
        state['infeedID'] = _normalize_keys(query.infeedid(safe=True))

        # Make sure we received values
        for label in labels:
            if bool(state[label]) is False:
                return
        if bool(state['infeedID']) is False:
            return

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


def main():
    """Start the infoset agent.

    Args:
        None

    Returns:
        None

    """
    # Get configuration
    cli = Agent.AgentCLI()
    poller = PollingAgent()

    # Do control
    cli.control(poller)


if __name__ == "__main__":
    main()
