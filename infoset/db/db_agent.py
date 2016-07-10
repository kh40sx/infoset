"""Module of infoset database functions.

Classes for agent data

"""

# Python standard libraries
from collections import defaultdict

# Infoset libraries
from infoset.log import log
from infoset.db import db


class Get(object):
    """Class to return agent data.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, uid, config):
        """Function for intializing the class.

        Args:
            uid: UID of agent
            config: Config object

        Returns:
            None

        """
        # Initialize important variables
        self.data_dict = defaultdict(dict)
        self.uid = uid

        # Prepare SQL query to read a record from the database.
        # Only active oids
        sql_query = (
            'SELECT iset_agent.idx, '
            'iset_agent.name, '
            'iset_agent.description, '
            'iset_agent.hostname, '
            'iset_agent.enabled '
            'FROM iset_agent '
            'WHERE '
            '(iset_agent.id="%s") LIMIT 1') % (
                uid)

        # Do query and get results
        database = db.Database(config)
        query_results = database.query(sql_query, 1038)

        # Massage data
        for row in query_results:
            # uid found?
            if not row[0]:
                log_message = ('uid %s not found.') % (uid)
                log.log2die(1302, log_message)

            # Assign values
            self.data_dict['idx'] = row[0]
            self.data_dict['name'] = row[1]
            self.data_dict['description'] = row[2]
            self.data_dict['hostname'] = row[3]
            self.data_dict['enabled'] = row[4]
            break

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

    def name(self):
        """Get agent name.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['name']
        return value

    def description(self):
        """Get agent description.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['description']
        return value

    def hostname(self):
        """Get agent hostname.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['hostname']
        return value

    def enabled(self):
        """Get agent enabled.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = bool(self.data_dict['enabled'])

        # Return
        return value
