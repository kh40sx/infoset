#!/usr/bin/env python3

"""Demonstration Script that extracts agent data from cache directory files.

This could be a modified to be a daemon

"""

# Standard libraries
import os
import sys
import time
import argparse

# Infoset libraries
from infoset.cache import cache
from infoset.utils import log
from infoset.utils import jm_configuration
from infoset.utils import hidden
from infoset.utils import Daemon


class IngestDaemon(Daemon):
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
        agent_name = 'ingestd'
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
            cache.process(self.config)
            time.sleep(60)


class IngestCLI(object):
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
            help='Stop the agent daemon.'
        )

        # CLI argument for starting
        parser.add_argument(
            '--start',
            required=False,
            default=False,
            action='store_true',
            help='Start the agent daemon.'
        )

        # CLI argument for restarting
        parser.add_argument(
            '--restart',
            required=False,
            default=False,
            action='store_true',
            help='Restart the agent daemon.'
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
        daemon = IngestDaemon(config)
        if args.start is True:
            daemon.start()
        elif args.stop is True:
            daemon.stop()
        elif args.restart is True:
            daemon.restart()
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
    cli = IngestCLI()
    config_dir = cli.config_dir()
    config = jm_configuration.ConfigServer(config_dir)

    # Do control
    cli.control(config)


if __name__ == "__main__":
    main()
