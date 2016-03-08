#!/usr/bin/env python3
"""Project Infoset CLI class."""

import textwrap
import argparse


class Cli(object):
    """Class gathers all CLI information.

    Args:
        None

    Returns:
        None

    Functions:
        __init__:
        get_cli:
    """

    def __init__(self, additional_help=None):
        """Function for intializing the class."""
        # Create a number of here-doc entries
        if additional_help is not None:
            self.config_help = additional_help
        else:
            self.config_help = ''

    def args(self):
        """Return all the CLI options.

        Args:
            self:

        Returns:
            args: Namespace() containing all of our CLI arguments as objects
                - filename: Path to the configuration file

        """
        # Initialize key variables
        width = 80

        # Header for the help menu of the application
        parser = argparse.ArgumentParser(
            description=self.config_help,
            formatter_class=argparse.RawTextHelpFormatter)

        # Add subparser
        subparsers = parser.add_subparsers(dest='mode')

        # Parse "config", return object used for parser
        _cli_config(subparsers, width=width)

        # Parse "pagemaker", return object used for parser
        _cli_pagemaker(subparsers, width=width)

        # Parse "poll", return object used for parser
        _cli_poll(subparsers, width=width)

        # Parse "test", return object used for parser
        _cli_test(subparsers, width=width)

        # Return the CLI arguments
        args = parser.parse_args()

        # Return our parsed CLI arguments
        return args


def _cli_config(subparsers, width=80):
    """Process "config" CLI commands.

    Args:
        subparsers: Subparsers object
        width: Width of the help text string to STDIO before wrapping

    Returns:
        None

    """
    # Initialize key variables
    parser = subparsers.add_parser(
        'config',
        help=textwrap.fill(
            'Print out configuration data.'
            '', width=width)
    )

    # Process directory
    parser.add_argument(
        '--directory',
        required=True,
        default=None,
        type=str,
        help=textwrap.fill(
            'Directory with configuration files.', width=width)
    )

    # Process hosts
    parser.add_argument(
        '--hosts',
        action='store_true',
        required=False,
        default=False,
        help=textwrap.fill(
            'Show list of hosts.', width=width)
    )

    # Process snmp_groups
    parser.add_argument(
        '--snmp_auth',
        action='store_true',
        required=False,
        default=False,
        help=textwrap.fill(
            'Show list of snmp_groups.', width=width)
    )


def _cli_test(subparsers, width=80):
    """Process "test" CLI commands.

    Args:
        subparsers: Subparsers object
        width: Width of the help text string to STDIO before wrapping

    Returns:
        None

    """
    # Initialize key variables
    parser = subparsers.add_parser(
        'test',
        help=textwrap.fill(
            'Query remote host for its data.', width=width)
    )

    # Process directory
    parser.add_argument(
        '--directory',
        required=True,
        default=None,
        type=str,
        help=textwrap.fill(
            'Directory with configuration files.', width=width)
    )

    # Process directory
    parser.add_argument(
        '--host',
        required=True,
        default=None,
        type=str,
        help=textwrap.fill(
            'Host to test.', width=width)
    )


def _cli_poll(subparsers, width=80):
    """Process "poll" CLI commands.

    Args:
        subparsers: Subparsers object
        width: Width of the help text string to STDIO before wrapping

    Returns:
        None

    """
    # Initialize key variables
    parser = subparsers.add_parser(
        'poll',
        help=textwrap.fill(
            'Process all configured hosts.', width=width)
    )

    # Process directory
    parser.add_argument(
        '--directory',
        required=True,
        default=None,
        type=str,
        help=textwrap.fill(
            'Directory with configuration files.', width=width)
    )

    # Process verbose
    parser.add_argument(
        '--verbose',
        dest='verbose',
        action='store_true',
        required=False,
        default=False,
        help=textwrap.fill(
            'Verbose Output.', width=width)
    )


def _cli_pagemaker(subparsers, width=80):
    """Process "pagemaker" CLI commands.

    Args:
        subparsers: Subparsers object
        width: Width of the help text string to STDIO before wrapping

    Returns:
        None

    """
    # Initialize key variables
    parser = subparsers.add_parser(
        'pagemaker',
        help=textwrap.fill(
            'Create web pages.', width=width)
    )

    # Process directory
    parser.add_argument(
        '--directory',
        required=True,
        default=None,
        type=str,
        help=textwrap.fill(
            'Directory with configuration files.', width=width)
    )

    # Process verbose
    parser.add_argument(
        '--verbose',
        dest='verbose',
        action='store_true',
        required=False,
        default=False,
        help=textwrap.fill(
            'Verbose Output.', width=width)
    )
