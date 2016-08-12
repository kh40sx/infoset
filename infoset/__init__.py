#!/usr/bin/env python3
"""Infoset setup.

Manages parameters required by all classes in the module.

"""

# Main python libraries
import os
import sys

# Infoset libraries
from infoset.utils import log

INFOSET = None

def main():
    """Process data.

    Args:
        None

    Returns:
        None

    """
    # Check the environment
    log.check_environment()


if __name__ == 'infoset':
    main()
