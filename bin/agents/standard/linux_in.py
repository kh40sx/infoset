#!/usr/bin/env python3
"""infoset Linux agent.

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
import logging
import socket
from time import sleep

# infoset libraries
try:
    from infoset.agents import agent as Agent
except:
    print('You need to set your PYTHONPATH to include the infoset library')
    sys.exit(2)
from infoset.utils import jm_configuration
from infoset.agents import data_linux

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
        self.agent_name = 'linux_in'

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
            self.upload()

            # Sleep
            sleep(300)

    def upload(self):
        """Post system data to the central server.

        Args:
            None

        Returns:
            None

        """
        # Get hostname
        hostname = socket.getfqdn()

        # Get the UID for the agent
        uid = Agent.get_uid(hostname)

        # Initialize key variables
        agent = Agent.Agent(uid, self.config, hostname)

        # Update agent with linux data
        data_linux.getall(agent)

        # Post data
        success = agent.post()

        # Purge cache if success is True
        if success is True:
            agent.purge()


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
