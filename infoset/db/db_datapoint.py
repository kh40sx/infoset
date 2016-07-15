"""Module of infoset database functions.

Classes for agent data

"""

# Python standard libraries
from collections import defaultdict

# Infoset libraries
from infoset.utils import log
from infoset.db import db


class Get(object):
    """Class to return agent data.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, did, config):
        """Function for intializing the class.

        Args:
            did: Datapoint id
            config: Config object

        Returns:
            None

        """
        # Initialize important variables
        self.data_dict = defaultdict(dict)

        # Prepare SQL query to read a record from the database.
        # Only active oids
        sql_query = (
            'SELECT '
            'idx, '
            'idx_agent, '
            'agent_label, '
            'agent_source, '
            'enabled, '
            'base_type, '
            'multiplier, '
            'last_timestamp '
            'FROM iset_datapoint '
            'WHERE '
            '(iset_datapoint.id=\'%s\') LIMIT 1') % (
                did)

        # Do query and get results
        database = db.Database(config)
        query_results = database.query(sql_query, 1052)
        # Massage data
        for row in query_results:
            # uid found?
            if not row[0]:
                log_message = ('did %s not found.') % (did)
                log.log2die(1047, log_message)
            # Assign values
            self.data_dict['idx'] = row[0]
            self.data_dict['idx_agent,'] = row[1]
            self.data_dict['agent_label'] = row[2]
            self.data_dict['agent_source'] = row[3]
            self.data_dict['enabled'] = row[4]
            self.data_dict['base_type'] = row[5]
            self.data_dict['multiplier'] = row[6]
            self.data_dict['last_timestamp'] = row[7]

            break

    def last_timestamp(self):
        """Get last_timestamp value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['last_timestamp']
        return value

    def multiplier(self):
        """Get multiplier value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['multiplier']
        return value

    def base_type(self):
        """Get base_type value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['base_type']
        return value

    def enabled(self):
        """Get enabled value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['enabled']
        return value

    def agent_source(self):
        """Get agent_source value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['agent_source']
        return value

    def idx(self):
        """Get idx value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['idx']
        return value

    def idx_agent(self):
        """Get idx_agent value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['idx_agent']
        return value

    def agent_label(self):
        """Get agent_label value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['agent_label']
        return value


class GetIDX(object):
    """Class to return datapoint data.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, idx, config):
        """Function for intializing the class.

        Args:
            idx: Datapoint Index
            config: Config object

        Returns:
            None

        """
        # Initialize important variables
        self.data_dict = defaultdict(dict)

        # Prepare SQL query to read a record from the database.
        # Only active oids
        sql_query = (
            'SELECT '
            'id, '
            'idx_agent, '
            'agent_label, '
            'agent_source, '
            'enabled, '
            'base_type, '
            'multiplier, '
            'last_timestamp '
            'FROM iset_datapoint '
            'WHERE '
            '(iset_datapoint.idx=\'%s\') LIMIT 1') % (
                idx)

        # Do query and get results
        database = db.Database(config)
        query_results = database.query(sql_query, 1053)
        # Massage data
        for row in query_results:
            # uid found?
            if not row[0]:
                log_message = ('idx %s not found.') % (idx)
                log.log2die(1048, log_message)
            # Assign values
            self.data_dict['id'] = row[0]
            self.data_dict['idx_agent,'] = row[1]
            self.data_dict['agent_label'] = row[2]
            self.data_dict['agent_source'] = row[3]
            self.data_dict['enabled'] = row[4]
            self.data_dict['base_type'] = row[5]
            self.data_dict['multiplier'] = row[6]
            self.data_dict['last_timestamp'] = row[7]

            break

    def last_timestamp(self):
        """Get last_timestamp value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['last_timestamp']
        return value

    def multiplier(self):
        """Get multiplier value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['multiplier']
        return value

    def base_type(self):
        """Get base_type value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['base_type']
        return value

    def enabled(self):
        """Get enabled value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['enabled']
        return value

    def agent_source(self):
        """Get agent_source value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['agent_source']
        return value

    def datapoint_id(self):
        """Get idx value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['id']
        return value

    def idx_agent(self):
        """Get idx_agent value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['idx_agent']
        return value

    def agent_label(self):
        """Get agent_label value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['agent_label']
        return value
