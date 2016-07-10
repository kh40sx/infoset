#!/usr/bin/env python3
"""Nagios check general library."""

import sys
import os
import datetime
import time

# Infoset imports
from infoset.utils import jm_configuration


def log2die_safe(code, message):
    """Log message to STDOUT only and die.

    Args:
        code: Message code
        message: Message text

    Returns:
        None

    """
    # Initialize key variables
    output = _message(code, message, True)
    print(output)
    sys.exit(2)


def log2quiet(code, message):
    """Log message to file only, but don't die.

    Args:
        code: Message code
        message: Message text

    Returns:
        None

    """
    # Log to screen and file
    _logit(code, message, error=False, verbose=False)


def log2see(code, message):
    """Log message to file and STDOUT, but don't die.

    Args:
        code: Message code
        message: Message text

    Returns:
        None

    """
    # Log to screen and file
    _logit(code, message, error=False)


def log2die(code, message):
    """Log to STDOUT and file, then die.

    Args:
        code: Error number
        message: Descriptive error string

    Returns:
        None
    """
    _logit(code, message, error=True)


def _logit(code, message, error=True, verbose=True):
    """Log to STDOUT and File.

    Args:
        code: Error number
        message: Descriptive error string
        error: Is this an error or not?
        verbose: Quiet or not

    Returns:
        None

    """
    # Initialize key variables
    output = _message(code, message, error)

    # Log the message
    if error is True:
        print(output)
        _update_logfile(message)
        sys.exit(3)
    else:
        if verbose is True:
            print(output)
        _update_logfile(message)


def _update_logfile(message):
    """Write message to logfile.

    Args:
        message: Message to write

    Returns:
        None

    """
    # Get log filename
    # config = jm_configuration.ConfigCommon(os.environ['INFOSET_CONFIGDIR'])
    # filename = config.log_file()
    filename = /tmp/infoset.log

    # Write to file
    with open(filename, 'a') as f_handle:
        f_handle.write(
            ('%s\n') % (message)
        )


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
        log2die_safe(1041, log_message)

    # Get configuration directory
    config_directory = os.environ['INFOSET_CONFIGDIR']
    if (os.path.exists(config_directory) is False) or (
            os.path.isdir(config_directory) is False):
        log_message = (
            'Environment variables $INFOSET_CONFIGDIR set to '
            'directory %s that does not exist'
            '') % (config_directory)
        log2die_safe(1042, log_message)


def _message(code, message, error=True):
    """Create a formatted message string.

    Args:
        code: Message code
        message: Message text
        error: If True, create a different message string

    Returns:
        output: Message result

    """
    # Initialize key variables
    time_object = datetime.datetime.fromtimestamp(time.time())
    timestring = time_object.strftime('%Y-%m-%d %H:%M:%S,%f')

    # Format string for error message, print and die
    if error is True:
        prefix = 'ERROR'
    else:
        prefix = 'STATUS'
    output = ('%s - %s - [%s] %s') % (timestring, prefix, code, message)

    # Return
    return output
