#!/usr/bin/env python3
"""Nagios SNMP auth class: Manages SNMP Auth Groups."""

import os.path
import yaml

# Import project libraries
from infoset.utils import jm_general


class ConfigReader(object):
    """Class gathers all configuration information.

    Args:
        None

    Returns:
        None

    Functions:
        __init__:
        hosts:
        snmp_auth:
    """

    def __init__(self, config_directory):
        """Function for intializing the class."""
        # Initialize key variables
        yaml_found = False
        yaml_from_file = ''
        all_yaml_read = ''

        # Check if config_directory exists
        if os.path.isdir(config_directory) is False:
            log_message = (
                'Configuration directory "%s" '
                'doesn\'t exist!' % config_directory)
            jm_general.logit(1009, log_message)

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
            jm_general.logit(1010, log_message)

        # Return
        self.config_dict = yaml.load(all_yaml_read)

    def hosts(self):
        """Get all hosts in the configuration file.

        Args:
            None

        Returns:
            hostnames: List of hostnames

        """
        # Initialize key variables
        hostnames = None

        # Process configuration
        if 'hosts' in self.config_dict:
            if isinstance(self.config_dict['hosts'], list) is True:
                hostnames = sorted(self.config_dict['hosts'])

        # Return
        return hostnames

    def snmp_auth(self):
        """Get list of dicts of SNMP information in configuration file.

        Args:
            group: Group name to filter results by

        Returns:
            snmp_data: List of SNMP data dicts found in configuration file.

        """
        # Initialize key variables
        snmp_data = None
        seed_dict = {}
        seed_dict['snmp_version'] = 2
        seed_dict['snmp_secname'] = None
        seed_dict['snmp_community'] = None
        seed_dict['snmp_authprotocol'] = None
        seed_dict['snmp_authpassword'] = None
        seed_dict['snmp_privprotocol'] = None
        seed_dict['snmp_privpassword'] = None
        seed_dict['snmp_port'] = 161

        # Read configuration's SNMP information. Return 'None' if none found
        if 'snmp_groups' in self.config_dict:
            if isinstance(self.config_dict['snmp_groups'], list) is True:
                if len(self.config_dict['snmp_groups']) < 1:
                    return None
            else:
                return None

        # Start populating information
        snmp_data = []
        for read_dict in self.config_dict['snmp_groups']:
            # Next entry if this is not a dict
            if isinstance(read_dict, dict) is False:
                continue

            # Assign good data
            new_dict = {}
            for key in seed_dict.keys():
                if key in read_dict:
                    new_dict[key] = read_dict[key]
                else:
                    new_dict[key] = seed_dict[key]

            # Convert relevant strings to integers
            new_dict['snmp_version'] = int(new_dict['snmp_version'])
            new_dict['snmp_port'] = int(new_dict['snmp_port'])

            # Append data to list
            snmp_data.append(new_dict)

        # Return
        return snmp_data

    def data_directory(self):
        """Determine the data_directory.

        Args:
            None

        Returns:
            value: configured data_directory

        """
        # Get parameter
        value = self.config_dict['data_directory']

        # Check if value exists
        if os.path.isdir(value) is False:
            log_message = (
                'data_directory: "%s" '
                'in configuration doesn\'t exist!') % (value)
            jm_general.logit(1007, log_message)

        # Return
        return value

    def web_directory(self):
        """Determine the web_directory.

        Args:
            None

        Returns:
            value: configured web_directory

        """
        # Get parameter
        value = self.config_dict['web_directory']

        # Check if value exists
        if os.path.isdir(value) is False:
            log_message = (
                'web_directory: "%s" '
                'in configuration doesn\'t exist!') % (value)
            jm_general.logit(1016, log_message)

        # Return
        return value

    def snmp_directory(self):
        """Determine the snmp_directory.

        Args:
            None

        Returns:
            value: Implied snmp_directory

        """
        # Get parameter
        value = ('%s/snmp') % self.data_directory()

        # Return
        return value

    def snmp_device_file(self, host):
        """Determine the snmp_device_file.

        Args:
            host: Hostname

        Returns:
            value: Implied snmp_device_file

        """
        # Get parameter
        value = ('%s/%s.yaml') % (self.snmp_directory(), host)

        # Return
        return value
