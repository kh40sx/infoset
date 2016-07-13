#!/usr/bin/env python3

"""Infoset ingest cache daemon.

Extracts agent data from cache directory files.

"""

# Standard libraries
import argparse
import os

# Infoset libraries
from infoset.db import db_chart
from infoset.utils import jm_configuration


def process():
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

    # CLI datapoint value
    parser.add_argument(
        '--idx_datapoint',
        required=True,
        type=int,
        help='Datapoint ID.'
    )

    # CLI argument for output filename
    parser.add_argument(
        '--filename',
        required=True,
        type=str,
        help='Output filename'
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
    # Get configuration
    args = process()
    idx_datapoint = args.idx_datapoint

    # Get configuration object
    config_dir = os.environ['INFOSET_CONFIGDIR']
    config = jm_configuration.ConfigServer(config_dir)

    # Chart data
    chart = db_chart.Chart(idx_datapoint, config,
        image_width=8,
        image_height=5)
    chart.single_line(
        'Test Chart', 'Data',
        '#0000FF', args.filename,
        )


if __name__ == "__main__":
    main()
