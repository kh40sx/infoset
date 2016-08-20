#!/usr/bin/env python3
"""Infoset ingest cache daemon.

Extracts agent data from cache directory files.

"""

# Standard libraries
import argparse

# Infoset libraries
from infoset.utils import metadata


def cli():
    """Return all the CLI options.

    Args:
        None

    Returns:
        args: Namespace() containing all of our CLI arguments as objects
            - filename: Path to the configuration file

    """
    # Header for the help menu of the application
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)

    # CLI argument for output filename
    parser.add_argument(
        '--directory',
        required=False,
        type=str,
        help=(
            'Directory with OID configuration yaml files for '
            'OIDs not supported by infoset by default.')
    )

    # Get the parser value
    args = parser.parse_args()
    return args


def main():
    """Process agent data.

    Args:
        None

    Returns:
        None

    """
    # Get additional directory to process
    cli_args = cli()
    directory = cli_args.directory

    # Process directory
    metadata.insert_oids(directory)


if __name__ == "__main__":
    main()
