#!/usr/bin/env python3

"""Demonstration Script that extracts agent data from cache directory files.

This could be a modified to be a daemon

"""

# Standard libraries
from threading import Timer
import argparse

# Infoset libraries
from infoset.cache import cache
from infoset.utils import jm_configuration


def process_cli(additional_help=None):
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

    # CLI argument for the config directory
    parser.add_argument(
        '--config_dir',
        dest='config_dir',
        required=True,
        default=None,
        type=str,
        help='Configuration directory.'
    )

    # Return the CLI arguments
    args = parser.parse_args()

    # Return our parsed CLI arguments
    return args


def main():
    """Process agent data.

    Args:
        None

    Returns:
        None

    """
    # Get configuration
    args = process_cli()

    # Get data from the cache directory
    config = jm_configuration.ConfigServer(args.config_dir)
    cache.process(config)

    # Do the daemon thing
    Timer(10, main).start()


if __name__ == "__main__":
    main()
