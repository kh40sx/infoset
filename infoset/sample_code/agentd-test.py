#!/usr/bin/env python3

"""Infoset ingest cache daemon.

Extracts agent data from cache directory files.

"""

# Standard libraries
import os
import time
from datetime import datetime

# Infoset libraries
from infoset.agents import check
from infoset.utils import jm_configuration


def main():
    """Process agent data.

    Args:
        None

    Returns:
        None

    """
    # Process Cache
    check.process()

if __name__ == "__main__":
    main()
