#!/usr/bin/env python3
"""Infoset setup.

Manages parameters required by all classes in the module.

"""

# Main python libraries
import os
import sys


def check_environment():
    """Check environmental variables. Die if incorrect.

    Args:
        None

    Returns:
        None

    """
    # Get environment
    if 'INFOSET_CONFIGDIR' not in os.environ:
        log_message = (
            'Environment variables $INFOSET_CONFIGDIR needs '
            'to be set to the infoset configuration directory.')
        print(log_message)
        sys.exit(4)

    # Verify configuration directory
    config_directory = os.environ['INFOSET_CONFIGDIR']
    if (os.path.exists(config_directory) is False) or (
            os.path.isdir(config_directory) is False):
        log_message = (
            'Environment variables $INFOSET_CONFIGDIR set to '
            'directory %s that does not exist'
            '') % (config_directory)
        print(log_message)
        sys.exit(4)


def main():
    """Process data.

    Args:
        None

    Returns:
        None

    """
    # Check the environment
    check_environment()


if __name__ == 'infoset':
    main()
