#!/usr/bin/env python3

"""Infoset ingest cache daemon.

Extracts agent data from cache directory files.

"""

# Standard libraries
import os
import sys
import time
import argparse

# Infoset libraries
from infoset.agents import check
from infoset.utils import log
from infoset.utils import jm_configuration
from infoset.utils import hidden
from infoset.utils import Daemon


class AgentCheckDaemon(Daemon):
    """Class that manages polling.

    Args:
        None

    Returns:
        None

    """

    def __init__(self, config):
        """Method initializing the class.

        Args:
            config: ConfigServer Object

        Returns:
            None

        """
        # Instantiate poller
        self.config = config

        # Get PID filename
        agent_name = '_agentsd'
        f_obj = hidden.File()
        self.pidfile = f_obj.pid(agent_name)

        # Call up the base daemon
        Daemon.__init__(self, self.pidfile)

    def run(self):
        """Start polling.

        Args:
            None

        Returns:
            None

        """
        # Do the daemon thing
        while True:
            check.process()
            time.sleep(15)


class AgentCheckCLI(object):
    """Class that manages the agent CLI.

    Args:
        None

    Returns:
        None

    """

    def __init__(self):
        """Method initializing the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        self.parser = None

        log.check_environment()
        self.config_directory = os.environ['INFOSET_CONFIGDIR']

    def config_dir(self):
        """Return configuration directory.

        Args:
            None

        Returns:
            value: Configuration directory

        """
        # Return
        value = self.config_directory
        return value

    def process(self, additional_help=None):
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

        # CLI argument for stopping
        parser.add_argument(
            '--stop',
            required=False,
            default=False,
            action='store_true',
            help='Stop the ingest daemon.'
        )

        # CLI argument for starting
        parser.add_argument(
            '--start',
            required=False,
            default=False,
            action='store_true',
            help='Start the ingest daemon.'
        )

        # CLI argument for restarting
        parser.add_argument(
            '--restart',
            required=False,
            default=False,
            action='store_true',
            help='Restart the ingest daemon.'
        )

        # CLI argument for statusing
        parser.add_argument(
            '--status',
            required=False,
            default=False,
            action='store_true',
            help='Get the status of the ingest daemon.'
        )

        # Get the parser value
        self.parser = parser

    def control(self, config):
        """Start the infoset agent.

        Args:
            config: ConfigServer Object

        Returns:
            None

        """
        # Get the CLI arguments
        self.process()
        parser = self.parser
        args = parser.parse_args()

        # Run daemon
        daemon = AgentCheckDaemon(config)
        if args.start is True:
            daemon.start()
        elif args.stop is True:
            daemon.stop()
        elif args.restart is True:
            daemon.restart()
        elif args.status is True:
            daemon.status()
        else:
            parser.print_help()
            sys.exit(2)


def main():
    """Process agent data.

    Args:
        None

    Returns:
        None

    """
    # Get configuration
    cli = AgentCheckCLI()
    config_dir = cli.config_dir()
    config = jm_configuration.ConfigServer(config_dir)

    # Do control
    cli.control(config)


if __name__ == "__main__":
    main()
