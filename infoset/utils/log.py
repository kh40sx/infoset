#!/usr/bin/env python3
"""Nagios check general library."""

import sys
import os
import datetime
import time
import getpass
import logging


# Infoset libraries
from infoset.utils import jm_configuration


def check_environment():
    """Check environmental variables. Die if incorrect.

    Args:
        None

    Returns:
        path: Path to config directory

    """
    # Get environment
    if 'INFOSET_CONFIGDIR' not in os.environ:
        log_message = (
            'Environment variables $INFOSET_CONFIGDIR needs '
            'to be set to the infoset configuration directory.')
        log2die_safe(1041, log_message)

    # Verify configuration directory
    config_directory = os.environ['INFOSET_CONFIGDIR']
    if (os.path.exists(config_directory) is False) or (
            os.path.isdir(config_directory) is False):
        log_message = (
            'Environment variables $INFOSET_CONFIGDIR set to '
            'directory %s that does not exist'
            '') % (config_directory)
        log2die_safe(1042, log_message)

    # Return
    path = os.environ['INFOSET_CONFIGDIR']
    return path


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


def log2warn(code, message):
    """Log warning message to file only, but don't die.

    Args:
        code: Message code
        message: Message text

    Returns:
        None

    """
    # Initialize key variables
    warning = ('WARNING - %s') % (message)
    _logit(code, warning, error=False, verbose=False)


def log2quiet(code, message):
    """Log status message to file only, but don't die.

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


def _logit(error_num, error_string, error=False, verbose=False):
    """Log slurpy errors to file and STDOUT.

    Args:
        error_num: Error number
        error_string: Descriptive error string
        error: Is this an error or not?
        verbose: If True print non errors to STDOUT

    Returns:
        None

    """
    # Define key variables
    app_name = 'infoset'
    username = getpass.getuser()

    # Get the logging directory
    config_directory = check_environment()
    config = jm_configuration.Config(config_directory)
    log_file = config.log_file()

    # create logger
    logger_file = logging.getLogger(('%s_file') % (app_name))
    logger_stdout = logging.getLogger(('%s_console') % (app_name))

    # Set logging levels to file and stdout
    logger_stdout.setLevel(logging.DEBUG)
    logger_file.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    file_handle = logging.FileHandler(log_file)
    file_handle.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    stdout_handle = logging.StreamHandler()
    stdout_handle.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s '
                                  '- %(levelname)s - %(message)s')
    file_handle.setFormatter(formatter)
    stdout_handle.setFormatter(formatter)

    # add the handlers to the logger
    logger_file.addHandler(file_handle)
    logger_stdout.addHandler(stdout_handle)

    # Log the message
    if error:
        log_message = (
            'ERROR [%s] (%sE): %s') % (
                username, error_num, error_string)
        logger_stdout.debug('%s', log_message)
        logger_file.debug(log_message)

        # Remove handler
        logger_file.removeHandler(file_handle)
        logger_stdout.removeHandler(stdout_handle)

        # Close handler
        file_handle.close()
        stdout_handle.close()

        # All done
        sys.exit(2)
    else:
        log_message = (
            'STATUS [%s] (%sS): %s') % (
                username, error_num, error_string)
        logger_file.debug(log_message)
        if verbose:
            logger_stdout.debug('%s', log_message)

    # Remove handler
    logger_file.removeHandler(file_handle)
    logger_stdout.removeHandler(stdout_handle)

    # Close handler
    file_handle.close()
    stdout_handle.close()


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
    username = getpass.getuser()

    # Format string for error message, print and die
    if error is True:
        prefix = 'ERROR'
    else:
        prefix = 'STATUS'
    output = ('%s - %s - %s - [%s] %s') % (
        timestring, username, prefix, code, message)

    # Return
    return output
