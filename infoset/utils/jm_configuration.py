#!/usr/bin/env python3
"""infoset classes that manage various configurations."""

import os.path
import os.environ

# Import project libraries
from infoset.utils import jm_general
from infoset.utils import log


class Config(object):
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

    def __init__(self):
        """Function for intializing the class.

        Args:
            None

        Returns:
            None

        """
        # Update the configuration directory
        # 'INFOSET_CONFIGDIR' is used for unittesting
        if 'INFOSET_CONFIGDIR' in os.environ:
            config_directory = os.environ['INFOSET_CONFIGDIR']
        else:
            config_directory = ('%s/etc') % (jm_general.root_directory())
        directories = [config_directory]

        # Return
        self.config_dict = jm_general.read_yaml_files(directories)

    def server(self):
        """Get server.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        sub_key = 'server'
        key = 'common'

        # Get new result
        value = _key_sub_key(key, sub_key, self.config_dict, die=False)
        result = bool(value)

        # Return
        return result

    def language(self):
        """Get language.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        sub_key = 'language'
        result = None
        key = 'common'

        # Get new result
        result = _key_sub_key(key, sub_key, self.config_dict)

        # Return
        return result

    def hosts(self):
        """Get all hosts in the configuration file.

        Args:
            None

        Returns:
            hostnames: List of hostnames

        """
        # Initialize key variables
        hostnames = None
        key = 'server'
        sub_key = 'hosts'

        # Process configuration
        hosts = _key_sub_key(key, sub_key, self.config_dict)
        if hosts is not None:
            if isinstance(hosts, list) is True:
                hostnames = sorted(hosts)

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
        key = 'server'
        sub_key = 'data_directory'

        # Get result
        value = _key_sub_key(key, sub_key, self.config_dict)

        # Determine whether path exists
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
        value = ('%s/%s.yaml') % (self.data_directory(), host)

        # Return
        return value

    def web_directory(self):
        """Determine the web_directory.

        Args:
            None

        Returns:
            value: configured web_directory

        """
        # Initialize key variables
        key = 'server'
        sub_key = 'web_directory'

        # Process configuration
        value = _key_sub_key(key, sub_key, self.config_dict)

        # Check if value exists
        if os.path.isdir(value) is False:
            log_message = (
                'web_directory: "%s" '
                'in configuration doesn\'t exist!') % (value)
            log.log2die(1093, log_message)

        # Return
        return value

    def ingest_cache_directory(self):
        """Determine the ingest_cache_directory.

        Args:
            None

        Returns:
            value: configured ingest_cache_directory

        """
        # Initialize key variables
        key = 'server'
        sub_key = 'ingest_cache_directory'

        # Process configuration
        value = _key_sub_key(key, sub_key, self.config_dict)

        # Check if value exists
        if os.path.isdir(value) is False:
            log_message = (
                'ingest_cache_directory: "%s" '
                'in configuration doesn\'t exist!') % (value)
            log.log2die(1030, log_message)

        # Return
        return value

    def ingest_failures_directory(self):
        """Determine the ingest_failures_directory.

        Args:
            None

        Returns:
            value: configured ingest_failures_directory

        """
        # Get parameter
        value = ('%s/failures') % (self.ingest_cache_directory())

        # Check if value exists
        if os.path.exists(value) is False:
            os.makedirs(value)

        # Return
        return value

    def db_name(self):
        """Get db_name.

        Args:
            None

        Returns:
            result: result

        """
        # Initialize key variables
        key = 'server'
        sub_key = 'db_name'

        # Process configuration
        result = _key_sub_key(key, sub_key, self.config_dict)

        # Get result
        return result

    def db_username(self):
        """Get db_username.

        Args:
            None

        Returns:
            result: result

        """
        # Initialize key variables
        key = 'server'
        sub_key = 'db_username'

        # Process configuration
        result = _key_sub_key(key, sub_key, self.config_dict)

        # Get result
        return result

    def db_password(self):
        """Get db_password.

        Args:
            None

        Returns:
            result: result

        """
        # Initialize key variables
        key = 'server'
        sub_key = 'db_password'

        # Process configuration
        result = _key_sub_key(key, sub_key, self.config_dict)

        # Get result
        return result

    def db_hostname(self):
        """Get db_hostname.

        Args:
            None

        Returns:
            result: result

        """
        # Initialize key variables
        key = 'server'
        sub_key = 'db_hostname'

        # Process configuration
        result = _key_sub_key(key, sub_key, self.config_dict)

        # Get result
        return result

    def agent_threads(self):
        """Get agent_threads.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = 'server'
        sub_key = 'agent_threads'
        result = _key_sub_key(key, sub_key, self.config_dict, die=False)

        # Default to 20
        if result is None:
            result = 20
        return result

    def ingest_threads(self):
        """Get ingest_threads.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = 'server'
        sub_key = 'ingest_threads'
        result = _key_sub_key(key, sub_key, self.config_dict, die=False)

        # Default to 20
        if result is None:
            result = 20
        return result

    def log_file(self):
        """Get log_file.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        sub_key = 'log_file'
        result = None
        key = 'common'

        # Get new result
        result = _key_sub_key(key, sub_key, self.config_dict)

        # Return
        return result

    def agents(self):
        """Get agents.

        Args:
            None

        Returns:
            result: list of agents

        """
        # Initialize key variables
        key = 'agents'
        result = None

        # Verify data
        if key not in self.config_dict:
            log_message = ('No agents configured')
            log.log2die(1100, log_message)

        # Process agents
        result = self.config_dict[key]

        # Return
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

    def __init__(self, agent_name):
        """Function for intializing the class.

        Args:
            agent_name: Name of agent used to get descriptions
                from configuration subdirectory

        Returns:
            None

        """
        # Update the configuration directory
        # 'INFOSET_CONFIGDIR' is used for unittesting
        if 'INFOSET_CONFIGDIR' in os.environ:
            config_directory = os.environ['INFOSET_CONFIGDIR']
        else:
            config_directory = ('%s/etc') % (jm_general.root_directory())
        directories = [config_directory]

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
        # Initialize key variables
        key = 'agents_common'
        sub_key = 'server_name'

        # Get result
        if self.agent_name() == '_infoset':
            result = 'localhost'
        else:
            result = _key_sub_key(key, sub_key, self.config_dict)
        return result

    def server_port(self):
        """Get server_port.

        Args:
            None

        Returns:
            result: result

        """
        # Initialize key variables
        key = 'agents_common'
        sub_key = 'server_port'

        # Get result
        result = _key_sub_key(key, sub_key, self.config_dict, die=False)
        if result is None:
            result = 5000
        return result

    def server_https(self):
        """Get server_https.

        Args:
            None

        Returns:
            result: result

        """
        # Initialize key variables
        key = 'agents_common'
        sub_key = 'server_https'

        # Get result
        result = _key_sub_key(key, sub_key, self.config_dict, die=False)
        if result is None:
            result = False
        return result

    def agent_cache_directory(self):
        """Determine the agent_cache_directory.

        Args:
            None

        Returns:
            value: configured agent_cache_directory

        """
        # Initialize key variables
        key = 'agents_common'
        sub_key = 'agent_cache_directory'

        # Get result
        value = _key_sub_key(key, sub_key, self.config_dict)

        # Check if value exists
        if os.path.isdir(value) is False:
            log_message = (
                'agent_cache_directory: "%s" '
                'in configuration doesn\'t exist!') % (value)
            log.log2die(1031, log_message)

        # Return
        return value

    def language(self):
        """Get language.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        sub_key = 'language'
        result = None
        key = 'common'

        # Get new result
        result = _key_sub_key(key, sub_key, self.config_dict)

        # Return
        return result

    def log_file(self):
        """Get log_file.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        sub_key = 'log_file'
        result = None
        key = 'common'

        # Get new result
        result = _key_sub_key(key, sub_key, self.config_dict)

        # Return
        return result

    def agent_enabled(self):
        """Get agent_enabled.

        Args:
            None

        Returns:
            result: result

        """
        # Get config
        agent_config = _agent_config(self.agent_name(), self.config_dict)

        # Get result
        if 'agent_enabled' in agent_config:
            result = agent_config['agent_enabled']
        else:
            result = False
        return result

    def agent_filename(self):
        """Get agent_filename.

        Args:
            None

        Returns:
            result: result

        """
        # Get config
        agent_config = _agent_config(self.agent_name(), self.config_dict)

        # Get result
        result = agent_config['agent_filename']
        return result

    def agent_hostnames(self):
        """Get agent_hostnames.

        Args:
            None

        Returns:
            result: result

        """
        # Get config
        agent_config = _agent_config(self.agent_name(), self.config_dict)

        # Get result
        if 'agent_hostnames' in agent_config:
            result = agent_config['agent_hostnames']
        else:
            result = []

        # Return
        return result

    def agent_port(self):
        """Get agent_port.

        Args:
            None

        Returns:
            result: result

        """
        # Get config
        agent_config = _agent_config(self.agent_name(), self.config_dict)

        # Get result
        if 'agent_port' in agent_config:
            result = agent_config['agent_port']
        else:
            result = []

        # Return
        return result

    def agent_metadata(self):
        """Get agent_metadata.

        Args:
            None

        Returns:
            result: result

        """
        # Get config
        agent_config = _agent_config(self.agent_name(), self.config_dict)

        # Get result
        if 'agent_metadata' in agent_config:
            result = agent_config['agent_metadata']
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

    def __init__(self):
        """Function for intializing the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        self.none = None

        # Update the configuration directory
        # 'INFOSET_CONFIGDIR' is used for unittesting
        if 'INFOSET_CONFIGDIR' in os.environ:
            config_directory = os.environ['INFOSET_CONFIGDIR']
        else:
            config_directory = ('%s/etc') % (jm_general.root_directory())
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


def _key_sub_key(key, sub_key, config_dict, die=True):
    """Get config parameter from YAML.

    Args:
        key: Primary key
        sub_key: Secondary key
        config_dict: Dictionary to explore
        die: Die if true and the result encountered is None

    Returns:
        result: result

    """
    # Get result
    result = None

    # Get new result
    if key in config_dict:
        if sub_key in config_dict[key]:
            result = config_dict[key][sub_key]

    # Error if not configured
    if result is None and die is True:
        log_message = (
            '%s:%s not defined in configuration') % (key, sub_key)
        log.log2die(1016, log_message)

    # Return
    return result


def _agent_config(agent_name, config_dict):
    """Get agent config parameter from YAML.

    Args:
        agent_name: Agent Name
        config_dict: Dictionary to explore
        die: Die if true and the result encountered is None

    Returns:
        result: result

    """
    # Get result
    key = 'agents'
    result = None

    # Get new result
    if key in config_dict:
        configurations = config_dict[key]
        for configuration in configurations:
            if 'agent_name' in configuration:
                if configuration['agent_name'] == agent_name:
                    result = configuration
                    break

    # Error if not configured
    if result is None:
        log_message = (
            'Agent %s not defined in configuration in '
            'agents:%s section') % (key, key)
        log.log2die(1094, log_message)

    # Return
    return result
