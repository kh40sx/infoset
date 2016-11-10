#!/usr/bin/env python3

"""Demonstration Script that extracts agent data from cache directory files.

This could be a modified to be a daemon

"""

# Standard libraries
import os
import re
import json
import time

# Infoset libraries
from infoset.utils import log
from infoset.utils import jm_general
from infoset.db import db_hostagent
from infoset.db import db_agent
from infoset.db import db_host


class ValidateCache(object):
    """Infoset class that ingests agent data.

    Args:
        None

    Returns:
        None

    Methods:
        __init__:
        populate:
        post:
    """

    def __init__(self, filepath=None, data=None):
        """Method initializing the class.

        Args:
            filepath: Cache filename
            data: Data dict expected to be in a cache file (Agent or server)

        Returns:
            None

        """
        # Initialize key variables
        self.validated = True
        self.information = {}
        self.filepath = filepath

        # Assign data to self.information for future validity checks
        if filepath is not None:
            # Read data from file
            self.information = _read_data_from_file(self.filepath)
        else:
            if isinstance(data, dict) is True:
                self.information = data

    def getinfo(self):
        """Provide validated information when valid.

        Args:
            None

        Returns:
            data: Data

        """
        # Initialize key variables
        data = False

        # Return
        if self.valid() is True:
            data = self.information
        return data

    def valid(self):
        """Master method that defines whether data is OK.

        Args:
            None

        Returns:
            all_ok:

        """
        # Initialize key variables
        validity = []
        ts_start = time.time()

        # Check primary keys
        validity.append(
            _check_primary_keys_exist(self.information))

        # Check timestamp key
        if False not in validity:
            validity.append(
                _check_timestamp_key(self.information))

        # Check validity of primary keys in file
        if False not in validity:
            validity.append(
                self._check_primary_keys_in_file())

        # Check chartable and unchartable data in the data
        if False not in validity:
            validity.append(_check_reported_data(self.information))
        if False not in validity:
            validity.append(_check_chartable_data(self.information))

        # Check if data to be validated is already in the database
        if False not in validity:
            validity.append(_check_duplicates(self.information))

        # Do final check
        if False in validity:
            # Log failure
            if self.filepath is None:
                mid_string = ''
            else:
                mid_string = ('in %s') % (self.filepath)
            log_message = ('Cache data %s is invalid') % (mid_string)
            log.log2warn(1059, log_message)
            all_ok = False
        else:
            # Log success
            ts_stop = time.time()
            duration = ts_stop - ts_start
            if self.filepath is None:
                mid_string = ''
            else:
                mid_string = ('of %s') % (self.filepath)
            log_message = (
                'Data validation %s took %s seconds.'
                '') % (mid_string, round(duration, 4))
            log.log2quiet(1126, log_message)
            all_ok = True

        # Return
        return all_ok

    def _check_primary_keys_in_file(self):
        """Validate the values of the primary JSON keys in the ingest file.

        Args:
            None

        Returns:
            valid: True if valid

        """
        # Initialize key variables
        valid = True
        filepath = self.filepath

        # Parse filename for information
        if self.filepath is not None:
            if _valid_filename(filepath) is True:
                filename = os.path.basename(filepath)
                (name, _) = filename.split('.')
                (tstamp, uid, _) = name.split('_')
                timestamp = int(tstamp)

                # Double check that the UID and timestamp in the
                # filename matches that in the file.
                # Ignore invalid files as a safety measure.
                # Don't try to delete. They could be owned by some
                # one else and the daemon could crash
                if uid != self.information['uid']:
                    log_message = (
                        'UID %s in file %s does not match UID %s in filename.'
                        '') % (self.information['uid'], uid, filepath)
                    log.log2warn(1123, log_message)
                    valid = False

                # Check timestamp
                if timestamp != self.information['timestamp']:
                    log_message = (
                        'Timestamp %s in file %s does not match timestamp '
                        '%s in filename.'
                        '') % (
                            self.information['timestamp'],
                            timestamp, filepath)
                    log.log2warn(1111, log_message)
                    valid = False

                # Check timestamp validity
                if jm_general.validate_timestamp(timestamp) is False:
                    log_message = (
                        'Timestamp %s in file %s is not normalized'
                        '') % (self.information['timestamp'], filepath)
                    log.log2warn(1112, log_message)
                    valid = False
            else:
                valid = False

        # Return
        return valid


def _check_chartable_data(information):
    """Check the data types being reported by the agent.

    Args:
        information: Data to analyze

    Returns:
        valid: True if valid

    """
    # Initialize key variables
    valid = True
    data_type = 'chartable'

    # Check that we are evaluating a dict
    if isinstance(information, dict) is False:
        log_message = ('Ingest data is not a dictionary')
        log.log2warn(1122, log_message)
        valid = False
        return valid

    # Check for chartable data
    if data_type in information:

        # Process the data type
        for _, reported_data in sorted(
                information[data_type].items()):

            # Make sure the base types are numeric
            if 'base_type' in reported_data:
                try:
                    float(reported_data['base_type'])
                except:
                    log_message = (
                        'Chartable "base_type" key is non numeric.')
                    log.log2warn(1120, log_message)
                    valid = False
            else:
                log_message = (
                    'Chartable data has no "base_type" key.')
                log.log2warn(1117, log_message)
                valid = False

            # Process data
            if 'data' in reported_data:
                for datapoint in reported_data['data']:
                    # Check to make sure value is numeric
                    value = datapoint[1]
                    try:
                        float(value)
                    except:
                        log_message = (
                            'Chartable data has non numeric data values.')
                        log.log2warn(1119, log_message)
                        valid = False
                        break
            else:
                log_message = (
                    'Chartable data has no "data" key.')
                log.log2warn(1118, log_message)
                valid = False

    # Return
    return valid


def _check_reported_data(information):
    """Check the data types being reported by the agent.

    Args:
        information: Data to analyze

    Returns:
        valid: True if valid

    """
    # Initialize key variables
    valid = True
    data_types = ['chartable', 'other']

    # Check that we are evaluating a dict
    if isinstance(information, dict) is False:
        log_message = ('Ingest data is not a dictionary')
        log.log2warn(1121, log_message)
        valid = False
        return valid

    # Process chartable data
    for data_type in data_types:
        # Skip if data type isn't in the data
        if data_type not in information:
            continue

        # Process the data type
        for _, reported_data in sorted(
                information[data_type].items()):
            # Process keys
            for key in ['base_type', 'description', 'data']:
                if key not in reported_data:
                    log_message = (
                        '"%s" data type does not contain a "%s" key.'
                        '') % (data_type, key)
                    log.log2warn(1115, log_message)
                    valid = False

            # Process data
            if 'data' in reported_data:
                for datapoint in reported_data['data']:
                    if len(datapoint) != 3:
                        log_message = (
                            '"%s" data type does not contain valid '
                            'datapoints in it\'s "data" key.'
                            '') % (data_type)
                        log.log2warn(1114, log_message)
                        valid = False

    # Return
    return valid


def _check_duplicates(information):
    """Check whether reported data reported is already in the database.

    Args:
        None

    Returns:
        valid: True if valid

    """
    # Initialize key variables
    valid = True

    # Check that we are evaluating a dict
    if isinstance(information, dict) is False:
        log_message = ('Ingest data is not a dictionary')
        log.log2warn(1116, log_message)
        valid = False
        return valid

    # Check that we have the correct keys in the dict
    if _check_primary_keys_exist(information) is False:
        valid = False
        return valid

    # Get values
    timestamp = int(information['timestamp'])
    uid = information['uid']
    hostname = information['hostname']

    # Check if there is a duplicate entry for this UID
    if db_agent.uid_exists(uid) is not False:
        idx_agent = db_agent.GetUID(uid).idx()

        # Check if host exists
        if db_host.hostname_exists(hostname) is True:
            idx_host = db_host.GetHost(hostname).idx()

            # Check for host / agent entry existence
            if db_hostagent.host_agent_exists(
                    idx_host, idx_agent) is True:
                # Check if this host / agent has been updated before
                last_timesamp = db_hostagent.GetHostAgent(
                    idx_host, idx_agent).last_timestamp()

                # Validate
                if timestamp <= last_timesamp:
                    log_message = (
                        'Data for UID %s, hostname %s at timestamp %s '
                        'is already found in database.'
                        '') % (uid, hostname, timestamp)
                    log.log2warn(1113, log_message)
                    valid = False

    # Return
    return valid


def _check_timestamp_key(information):
    """Check whether timestamp key is an integer value.

    Args:
        information: Dict of JSON data

    Returns:
        valid: True if valid

    """
    # Initialize key variables
    valid = True
    key = 'timestamp'

    # Verify we have a dictionary
    if isinstance(information, dict) is False:
        log_message = ('Ingest data is not a dictionary')
        log.log2warn(1110, log_message)
        valid = False
    else:
        # Timestamp must be an integer
        try:
            if key in information:
                int(information[key])
        except:
            log_message = ('Ingest data has no valid timestamp key')
            log.log2warn(1047, log_message)
            valid = False

    # Return
    return valid


def _check_primary_keys_exist(information):
    """Check whether primary keys exist in json.

    Args:
        information: Data dictionary to check

    Returns:
        valid: True if valid

    """
    # Initialize key variables
    valid = True
    agent_meta_keys = ['timestamp', 'uid', 'agent', 'hostname']

    # Verify we have a dictionary
    if isinstance(information, dict) is False:
        log_message = ('Ingest data is not a dictionary')
        log.log2warn(1093, log_message)
        valid = False
    else:
        # Verify keys in information
        for key in agent_meta_keys:
            if key not in information:
                # Log status and stop processing
                valid = False
                log_message = ('Ingest data does not have a %s key.') % (key)
                log.log2warn(1039, log_message)
                break

    # Return
    return valid


def _valid_filename(filepath):
    """Check if the filename in the filepath is valid.

    Args:
        filepath: Filepath

    Returns:
        valid: True if valid

    """
    # Initialize key variables
    valid = False

    # Filenames must start with a numeric timestamp and #
    # end with a hex string. This will be tested later
    regex = re.compile(r'^\d+_[0-9a-f]+_[0-9a-f]+.json')

    # Try reading file if filename format is OK
    filename = os.path.basename(filepath)
    if bool(regex.match(filename)) is True:
        valid = True

    # Return
    return valid


def _read_data_from_file(filepath):
    """Provide validated information when valid.

    Args:
        filepath: Path to file

    Returns:
        data: Data

    """
    # Initialize key variables
    data = {}

    # Try reading file if filename format is OK
    if _valid_filename(filepath) is True:
        # Ingest data
        try:
            with open(filepath, 'r') as f_handle:
                data = json.load(f_handle)
        except:
            # Log status
            log_message = (
                'File %s does not contain JSON data, does not exist, '
                'or is unreadable.') % (filepath)
            log.log2warn(1006, log_message)

    else:
        # Log status
        log_message = (
            'File %s does has incorrect filename format.'
            '') % (filepath)
        log.log2warn(1026, log_message)

    # Return
    return data
