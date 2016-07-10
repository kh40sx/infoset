#!/usr/bin/env python3
"""infoset classes that manage various configurations."""

import os.path

# Import project libraries
from infoset.utils import jm_general
from infoset.log import log


class ConfigCommon(object):
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

    def __init__(self, root_directory):
        """Function for intializing the class.

        Args:
            root_directory: Root configuration directory

        Returns:
            None

        """
        # Update the configuration directory
        common_directory = ('%s/common') % (root_directory)
        directories = [common_directory]

        # Return
        self.config_dict = jm_general.read_yaml_files(directories)

    def log_file(self):
        """Get log_file.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self.config_dict['log_file']
        return result


class ConfigServer(object):
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

    def __init__(self, root_directory):
        """Function for intializing the class.

        Args:
            root_directory: Root configuration directory

        Returns:
            None

        """
        # Update the configuration directory
        server_directory = ('%s/server') % (root_directory)
        common_directory = ('%s/common') % (root_directory)
        directories = [server_directory, common_directory]

        # Return
        self.config_dict = jm_general.read_yaml_files(directories)

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
            log.log2die(1007, log_message)

        # Return
        return value

    def snmp_directory(self):
        """Determine the snmp_directory.

        Args:
            None

        Returns:
            value: configured snmp_directory

        """
        # Get parameter
        value = ('%s/snmp') % (self.data_directory())

        # Create directory if neccessary
        if (os.path.isdir(self.data_directory()) is True) and (
                os.path.isdir(value) is False):
            os.mkdir(value)

        # Return
        return value

    def snmp_device_file(self, host):
        """Determine the snmp_device_file.

        Args:
            host: Hostname

        Returns:
            value: configured snmp_device_file

        """
        # Get parameter
        value = ('%s/%s.yaml') % (self.snmp_directory(), host)

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
            log.log2die(1016, log_message)

        # Return
        return value

    def ingest_cache_directory(self):
        """Determine the ingest_cache_directory.

        Args:
            None

        Returns:
            value: configured ingest_cache_directory

        """
        # Get parameter
        value = self.config_dict['ingest_cache_directory']

        # Check if value exists
        if os.path.isdir(value) is False:
            log_message = (
                'ingest_cache_directory: "%s" '
                'in configuration doesn\'t exist!') % (value)
            log.log2die(1030, log_message)

        # Return
        return value

    def db_name(self):
        """Get db_name.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self.config_dict['db_name']
        return result

    def db_username(self):
        """Get db_username.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self.config_dict['db_username']
        return result

    def db_password(self):
        """Get db_password.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self.config_dict['db_password']
        return result

    def db_hostname(self):
        """Get db_hostname.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self.config_dict['db_hostname']
        return result

    def ingest_threads(self):
        """Get ingest_threads.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self.config_dict['ingest_threads']
        return result

    def log_file(self):
        """Get log_file.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self.config_dict['log_file']
        return result


class ConfigAgent(object):
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

    def __init__(self, root_directory, agent_name):
        """Function for intializing the class.

        Args:
            root_directory: Root configuration directory
            agent_name: Name of agent used to get descriptions
                from configuration subdirectory

        Returns:
            None

        """
        # Update the configuration directory
        agent_directory = ('%s/agents') % (root_directory)
        descriptions_directory = ('%s/%s') % (agent_directory, agent_name)
        common_directory = ('%s/common') % (root_directory)
        directories = [
            agent_directory, descriptions_directory, common_directory]

        # Return
        self.config_dict = jm_general.read_yaml_files(directories)
        self.name = agent_name

    def agent_name(self):
        """Get agent_name.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self.name
        return result

    def server_name(self):
        """Get server_name.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self.config_dict['server_name']
        return result

    def server_port(self):
        """Get server_port.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self.config_dict['server_port']
        return result

    def server_https(self):
        """Get server_https.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self.config_dict['server_https']
        return result

    def log_file(self):
        """Get log_file.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self.config_dict['log_file']
        return result

    def agent_cache_directory(self):
        """Determine the agent_cache_directory.

        Args:
            None

        Returns:
            value: configured agent_cache_directory

        """
        # Get parameter
        value = self.config_dict['agent_cache_directory']

        # Check if value exists
        if os.path.isdir(value) is False:
            log_message = (
                'agent_cache_directory: "%s" '
                'in configuration doesn\'t exist!') % (value)
            log.log2die(1031, log_message)

        # Return
        return value

    def agent_source_descriptions(self):
        """Get agent_source_descriptions.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self.config_dict['agent_source_descriptions']
        return result

    def agent_snmp_hostnames(self):
        """Get agent_snmp_hostnames.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        if 'agent_snmp_hostnames' in self.config_dict:
            result = self.config_dict['agent_snmp_hostnames']
        else:
            result = []

        # Return
        return result


class ConfigSNMP(object):
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

    def __init__(self, root_directory):
        """Function for intializing the class.

        Args:
            root_directory: Root configuration directory

        Returns:
            None

        """
        # Initialize key variables
        self.none = None

        # Update the configuration directory
        config_directory = ('%s/snmp') % (root_directory)
        directories = [config_directory]

        # Return
        self.config_dict = jm_general.read_yaml_files(directories)

    def snmp_auth(self):
        """Get list of dicts of SNMP information in configuration file.

        Args:
            group: Group name to filter results by

        Returns:
            snmp_data: List of SNMP data dicts found in configuration file.

        """
        # Initialize key variables
        seed_dict = {}
        seed_dict['snmp_version'] = 2
        seed_dict['snmp_secname'] = None
        seed_dict['snmp_community'] = None
        seed_dict['snmp_authprotocol'] = None
        seed_dict['snmp_authpassword'] = None
        seed_dict['snmp_privprotocol'] = None
        seed_dict['snmp_privpassword'] = None
        seed_dict['snmp_port'] = 161
        seed_dict['group_name'] = None

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

    def dont_use(self):
        """Dummy method to pass linter.

        Args:
            None

        Returns:
            none: Nothing

        """
        # Initialize key variables
        none = self.none
        return none
