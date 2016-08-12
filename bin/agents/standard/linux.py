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
from time import sleep

# Pip3 libraries
import requests

# infoset libraries
try:
    from infoset.agents import agent as Agent
except:
    print('You need to set your PYTHONPATH to include the infoset library')
    sys.exit(2)
from infoset.utils import jm_configuration

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
            config_dir: Configuration directory

        Returns:
            None

        """
        # Initialize key variables
        self.agent_name = 'linux'

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
        self.config = jm_configuration.ConfigAgent(
            config_dir, self.agent_name)

    def query(self):
        """Query all remote hosts for data.

        Args:
            None

        Returns:
            None

        """
        # Define key variables
        get_success = False
        response = False
        uid = Agent.get_uid(self.hostname)

        # Create url
        url = ('http://%s:5001') % (self.hostname)

        # Post data save to cache if this fails
        try:
            result = requests.get(url)
            response = True
        except:
            response = False

        # Define success
        if response is True:
            if result.status_code == 200:
                get_success = True

        if get_success is True:
            # Initialize key variables
            agent = Agent.Agent(uid, self.config, self.hostname)

            # Post data
            post_success = agent.post(data=result.text)

            # Purge cache if success is True
            if post_success is True:
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
