#!/usr/bin/env python3

"""Infoset ingest cache daemon.

Extracts agent data from cache directory files.

"""

# Standard libraries
import os
import sys
import time
from datetime import datetime

# Infoset libraries
sys.path.append(
    '/home/simiya/users/peter/GitHub/infoset/bin/agents/standard')
from linux_passive import PollingAgent


def main():
    """Process agent data.

    Args:
        None

    Returns:
        None

    """
    # Process Cache
    poller = PollingAgent()
    poller.query()

if __name__ == "__main__":
    main()
