#!/usr/bin/env python3
"""Infoset general library."""

import os
import shutil
import json
import time
import yaml

# Infoset libraries
from infoset.utils import log


def validate_timestamp(timestamp):
    """Validate timestamp to be a multiple of 300 seconds.

    Args:
        timestamp: epoch timestamp in seconds

    Returns:
        valid: True if valid

    """
    # Initialize key variables
    valid = False

    # Process data
    test = (int(timestamp) // 300) * 300
    if test == timestamp:
        valid = True

    # Return
    return valid


def normalized_timestamp(timestamp=None):
    """Normalize timestamp to a multiple of 300 seconds.

    Args:
        timestamp: epoch timestamp in seconds

    Returns:
        value: Normalized value

    """
    # Process data
    if timestamp is None:
        value = (int(time.time()) // 300) * 300
    else:
        value = (int(timestamp) // 300) * 300
    # Return
    return value


def dict2yaml(data_dict):
    """Convert a dict to a YAML string.

    Args:
        data_dict: Data dict to convert

    Returns:
        yaml_string: YAML output
    """
    # Process data
    json_string = json.dumps(data_dict)
    yaml_string = yaml.dump(yaml.load(json_string), default_flow_style=False)

    # Return
    return yaml_string


def move_files(source_dir, target_dir):
    """Delete files in a directory.

    Args:
        source_dir: Directory where files are currently
        target_dir: Directory where files need to be

    Returns:
        Nothing

    """
    # Make sure source directory exists
    if os.path.exists(source_dir) is False:
        log_message = ('Directory %s does not exist.') % (
            source_dir)
        log.log2die(1011, log_message)

    # Make sure target directory exists
    if os.path.exists(target_dir) is False:
        log_message = ('Directory %s does not exist.') % (
            target_dir)
        log.log2die(1012, log_message)

    source_files = os.listdir(source_dir)
    for filename in source_files:
        full_path = ('%s/%s') % (source_dir, filename)
        shutil.move(full_path, target_dir)


def delete_files(target_dir):
    """Delete files in a directory.

    Args:
        target_dir: Directory in which files must be deleted

    Returns:
        Nothing

    """
    # Make sure target directory exists
    if os.path.exists(target_dir) is False:
        log_message = ('Directory %s does not exist.') % (
            target_dir)
        log.log2die(1013, log_message)

    # Delete all files in the tmp folder
    for the_file in os.listdir(target_dir):
        file_path = os.path.join(target_dir, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as exception_error:
            log_message = ('Error: deleting files in %s. Error: %s') % (
                target_dir, exception_error)
            log.log2die(1014, log_message)
        except:
            log_message = ('Unexpected error')
            log.log2die(1015, log_message)


def cleanstring(data):
    """Remove multiple whitespaces and linefeeds from string.

    Args:
        data: String to process

    Returns:
        result: Stipped data

    """
    # Initialize key variables
    nolinefeeds = data.replace('\n', ' ').replace('\r', '').strip()
    words = nolinefeeds.split()
    result = ' '.join(words)

    # Return
    return result


def read_yaml_files(directories):
    """Read the contents of all yaml files in a directory.

    Args:
        directories: List of directory names with configuration files

    Returns:
        config_dict: Dict of yaml read

    """
    # Initialize key variables
    yaml_found = False
    yaml_from_file = ''
    all_yaml_read = ''

    # Check each directory in sequence
    for config_directory in directories:
        # Check if config_directory exists
        if os.path.isdir(config_directory) is False:
            log_message = (
                'Configuration directory "%s" '
                'doesn\'t exist!' % config_directory)
            log.log2die(1009, log_message)

        # Cycle through list of files in directory
        for filename in os.listdir(config_directory):
            # Examine all the '.yaml' files in directory
            if filename.endswith('.yaml'):
                # YAML files found
                yaml_found = True

                # Read file and add to string
                file_path = ('%s/%s') % (config_directory, filename)
                with open(file_path, 'r') as file_handle:
                    yaml_from_file = file_handle.read()

                # Append yaml from file to all yaml previously read
                all_yaml_read = ('%s\n%s') % (all_yaml_read, yaml_from_file)

        # Verify YAML files found in directory
        if yaml_found is False:
            log_message = (
                'No files found in directory "%s" with ".yaml" '
                'extension.') % (config_directory)
            log.log2die(1010, log_message)

    # Return
    config_dict = yaml.load(all_yaml_read)
    return config_dict
