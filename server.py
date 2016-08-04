#! /usr/bin/env python3
from www import infoset
import os
import argparse
import sys
import time
from infoset.utils import Daemon
from infoset.utils import hidden
from infoset.utils import log


class ServerDaemon(Daemon):

    def __init__(self):
        f_obj = hidden.File()
        self.pidfile = f_obj.pid("server")
        self.server = infoset
        # Call up the base daemon
        Daemon.__init__(self, self.pidfile)
    
    def run(self):
        while True:
            print("From Server")
            self.server.run(debug=True, host='0.0.0.0', threaded=True) 


class ServerCLI(object):
    """Class that manages the server CLI.

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

        # Check environment
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

        # CLI argument for starting
        parser.add_argument(
            '--status',
            required=False,
            default=False,
            action='store_true',
            help='Get daemon daemon status.'
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

    def control(self, daemon):
        """Start the infoset agent.

        Args:
            poller: ServerDaemon object

        Returns:
            None

        """
        # Get the CLI arguments
        self.process()
        parser = self.parser
        args = parser.parse_args()

        # Run daemon
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
    """Start the infoset server.

    Args:
        None

    Returns:
        None

    """
    # Get configuration
    cli = ServerCLI()
    daemon = ServerDaemon()
    # Do control
    cli.control(daemon)


if __name__ == "__main__":
    main()
