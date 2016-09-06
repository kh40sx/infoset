#!/usr/bin/env python3
"""Infoset ingest cache daemon.

Extracts agent data from cache directory files.

"""

# Standard libraries
import sys
import os
import tempfile

# infoset libraries
try:
    from infoset.agents import agent as Agent
except:
    print('You need to set your PYTHONPATH to include the infoset library')
    sys.exit(2)
from infoset.utils import jm_configuration
from infoset.utils import jm_general
from infoset.utils import log
from infoset.snmp import snmp_info
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
        self.agent_name = 'topology'

        # Get configuration
        self.config = jm_configuration.ConfigAgent(self.agent_name)
        server_config = jm_configuration.Config()

        # Cleanup, move temporary files to clean permanent directory.
        # Delete temporary directory
        self.perm_dir = server_config.data_directory()
        if os.path.isdir(self.perm_dir):
            jm_general.delete_files(self.perm_dir)
        else:
            os.makedirs(self.perm_dir, 0o755)

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
        # Initialize key variables
        delay = 3600

        # Post data to the remote server
        while True:
            self._poll()

            # Sleep for "delay" seconds
            Agent.agent_sleep(self.name(), delay)

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
            # Add poller
            poller = Poller(hostname, self.agent_name, self.perm_dir)
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

    def __init__(self, hostname, agent_name, perm_dir):
        """Method initializing the class.

        Args:
            hostname: Hostname to poll
            agent_name: Name of agent
            perm_dir: Directory where permanent YAML files should reside.

        Returns:
            None

        """
        # Initialize key variables
        self.agent_name = agent_name
        self.hostname = hostname
        self.perm_dir = perm_dir

        # Get configuration
        config = jm_configuration.ConfigAgent(self.agent_name)

        # Initialize key variables
        self.agent = Agent.Agent(config, hostname)

        # Get snmp configuration information from infoset
        snmp_config = jm_configuration.ConfigSNMP()
        validate = snmp_manager.Validate(hostname, snmp_config.snmp_auth())
        self.snmp_params = validate.credentials()
        self.snmp_object = snmp_manager.Interact(self.snmp_params)

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
            self._create_yaml()
        else:
            log_message = (
                'Uncontactable host %s or no valid SNMP '
                'credentials found for it.') % (self.hostname)
            log.log2quiet(1019, log_message)

    def _create_yaml(self):
        """Create the master dictionary for the host.

        Args:
            None
        Returns:
            value: Index value

        """
        # Initialize key variables
        temp_dir = tempfile.mkdtemp()

        # Get data
        log_message = (
            'Querying topology data from host %s.'
            '') % (self.hostname)
        log.log2quiet(1019, log_message)

        status = snmp_info.Query(self.snmp_object)
        data = status.everything()
        yaml_string = jm_general.dict2yaml(data)

        # Dump data
        temp_file = ('%s/%s.yaml') % (temp_dir, self.hostname)
        with open(temp_file, 'w') as file_handle:
            file_handle.write(yaml_string)

        # Get data
        log_message = (
            'Completed topology query from host %s.'
            '') % (self.hostname)
        log.log2quiet(1019, log_message)

        # Clean up files
        jm_general.move_files(temp_dir, self.perm_dir)
        os.rmdir(temp_dir)


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
