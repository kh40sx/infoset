#!/usr/bin/env python3

"""Infoset ingest cache daemon.

Extracts agent data from cache directory files.

"""

# Standard libraries
import os
import time
from datetime import datetime

# Infoset libraries
from infoset.cache import cache
from infoset.utils import jm_configuration


def main():
    """Process agent data.

    Args:
        None

    Returns:
        None

    """
    # Get configuration
    config_directory = os.environ['INFOSET_CONFIGDIR']
    config = jm_configuration.ConfigServer(config_directory)

    # Do the daemon thing
    while True:
        # Print timestamp
        print(
            datetime.fromtimestamp(
                int(time.time())
            ).strftime('%Y-%m-%d %H:%M:%S')
        )

        # Process Cache
        cache.process(config)
        time.sleep(15)

if __name__ == "__main__":
    main()
