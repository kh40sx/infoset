#!/usr/bin/env python3
"""Nagios check general library."""

import sys
import os


def logit(error_num, error_string, is_error=True):
    """Log to STDOUT.

    Args:
        error_num: Error number
        error_string: Descriptive error string
        is_error: Is this an error or not?

    Returns:
        None
    """
    # Log the message
    if is_error is True:
        meta_message = ('(%s): %s') % (error_num, error_string)
        log_message = ('ERROR %s') % (meta_message)
        print(log_message)
        sys.exit(3)
    else:
        meta_message = ('(%sS): %s') % (error_num, error_string)
        log_message = ('STATUS %s') % (meta_message)
        print(log_message)
