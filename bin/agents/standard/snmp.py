#!/usr/bin/env python3
"""Infoset ingest cache daemon.

Extracts agent data from cache directory files.

"""

# Standard libraries
import os
import sys
from collections import defaultdict
from time import sleep

# infoset libraries
try:
    from infoset.agents import agent as Agent
except:
    print('You need to set your PYTHONPATH to include the infoset library')
    sys.exit(2)
from infoset.utils import jm_configuration
from infoset.utils import jm_general
from infoset.utils import log
from infoset.db import db_oid
from infoset.db import db_host
from infoset.db import db_hostoid
from infoset.snmp import snmp_manager


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
            config_dir: Configuration directory

        Returns:
            None

        """
        # Initialize key variables
        self.agent_name = 'snmp'

        # Get configuration
        config_dir = os.environ['INFOSET_CONFIGDIR']
        self.config = jm_configuration.ConfigAgent(
            config_dir, self.agent_name)

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

        # Create a list of polling objects
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
        config = jm_configuration.ConfigAgent(
            config_dir, self.agent_name)

        # Initialize key variables
        self.agent = Agent.Agent(config, hostname)

        # Get snmp configuration information from infoset
        snmp_config = jm_configuration.ConfigSNMP(config_dir)
        validate = snmp_manager.Validate(hostname, snmp_config.snmp_auth())
        self.snmp_params = validate.credentials()

    def query(self):
        """Query all remote hosts for data.

        Args:
            None

        Returns:
            None

        """
        # Check SNMP supported
        if bool(self.snmp_params) is True:
            # Get datapoints
            self._datapoints()

    def _datapoints(self):
        """Create the master dictionary for the host.

        Args:
            None
        Returns:
            value: Index value

        """
        # Initialize key variables
        snmp_params = self.snmp_params
        master = self._master()

        # Get sources
        snmp_object = snmp_manager.Interact(snmp_params)
        for labels_oid in master.keys():
            sources = {}
            oid_results = snmp_object.swalk(labels_oid)

            # Return if there is an error
            if bool(oid_results) is False:
                log_message = (
                    'Failed to contact SNMP host %s. '
                    'Will collect data on next poll.'
                    '') % (self.hostname)
                log.log2warn(1024, log_message)
                return

            for key, value in oid_results.items():
                sources[_index(labels_oid, key)] = jm_general.decode(value)

        # Get values
        for labels_oid in master.keys():
            for agent_label in master[labels_oid].keys():
                # Initialize datapoints
                datapoints = defaultdict(lambda: defaultdict(dict))

                # Information about the OID
                values_oid = master[labels_oid][agent_label]['values_oid']
                base_type = master[labels_oid][agent_label]['base_type']
                multiplier = master[labels_oid][agent_label]['multiplier']

                # Get OID values
                values = {}
                oid_results = snmp_object.swalk(values_oid)

                # Return if there is an error
                if bool(oid_results) is False:
                    log_message = (
                        'Failed to contact SNMP host %s. '
                        'Will collect data on next poll.'
                        '') % (self.hostname)
                    log.log2warn(1022, log_message)
                    return

                # Only process floating point values
                for key, value in oid_results.items():
                    try:
                        _ = float(value)
                    except:
                        continue
                    values[_index(labels_oid, key)] = value * multiplier

                # Create list of data for json
                data = []
                for index, value in values.items():
                    data.append([index, value, sources[index]])

                # Finish up dict for json
                datapoints[agent_label]['data'] = data
                datapoints[agent_label]['base_type'] = base_type

                # Populate agent
                self.agent.populate(datapoints)

        # Post data
        self.agent.post()

    def _master(self):
        """Create the master dictionary for the host.

        Args:
            None

        Returns:
            master: Master dictionary

        """
        # Initialize key variables
        hostname = self.hostname
        master = defaultdict(lambda: defaultdict(dict))

        # Get all oid IDX values tied to the hostname
        idx_host = db_host.GetHost(hostname).idx()
        oid_indices = db_hostoid.oid_indices(idx_host)

        # Get OID metadata
        for idx_oid in oid_indices:
            oid_object = db_oid.GetIDX(idx_oid)

            # Assign OIDs for values to the OID that
            # will be used to label the results
            labels_oid = oid_object.oid_labels()
            values_oid = oid_object.oid_values()
            agent_label = oid_object.agent_label()
            base_type = oid_object.base_type()
            multiplier = oid_object.multiplier()

            # Stuff to do
            master[labels_oid][agent_label]['values_oid'] = values_oid
            master[labels_oid][agent_label]['base_type'] = base_type
            master[labels_oid][agent_label]['multiplier'] = multiplier

        # Return
        return master


def _index(labels_oid, oid):
    """Find the index value of an OID.

    Args:
        labels_oid: OID used for labels
        oid: OID value

    Returns:
        value: Index value

    """
    # Initialize key variables
    value = None

    # Get all the nodes in the oids
    nodes_label = labels_oid.split('.')
    nodes_oid = oid.split('.')

    # Calculate the difference in lenth in terms of OID nodes
    nodes_in_index = len(nodes_oid) - len(nodes_label)

    # Calculate what the index should be
    value_nodes = nodes_oid[-nodes_in_index:]
    if nodes_in_index == 1:
        value = int(value_nodes[0])
    else:
        value = '.'.join(value_nodes)

    # Return
    return value


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
