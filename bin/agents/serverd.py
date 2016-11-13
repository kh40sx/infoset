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
import logging

# infoset libraries
try:
    from infoset.agents import agent as Agent
except:
    print('You need to set your PYTHONPATH to include the infoset library')
    sys.exit(2)
from infoset.utils import jm_configuration
from infoset.utils import log
from www import infoset


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
        self.agent_name = 'serverd'

        # Get configuration
        self.config = jm_configuration.ConfigAgent(self.agent_name)

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
        port = self.config.agent_port()

        # Set logging
        log_file = self.config.log_file()
        logging.basicConfig(filename=log_file, level=logging.DEBUG)

        # Post data to the remote server
        infoset.run(
            debug=True, host='0.0.0.0',
            threaded=True, port=port)


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
