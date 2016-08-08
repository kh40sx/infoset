"""Module of infoset database functions.

Classes for agent data

"""
# Python standard libraries
from collections import defaultdict

# Infoset libraries
from infoset.utils import log
from infoset.db import db
from infoset.db import POOL
from infoset.db.db_orm import Agent


class Get(object):
    """Class to return agent data.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, uid):
        """Function for intializing the class.

        Args:
            uid: UID of agent

        Returns:
            None

        """
        # Initialize important variables
        self.data_dict = defaultdict(dict)
        self.uid = uid

        # Establish a database session
        session = POOL()
        query = session.query(Agent).filter(Agent.id == uid)

        # Massage data
        if query.count() == 1:
            for instance in query:
                self.data_dict['idx'] = instance.idx
                self.data_dict['name'] = instance.name
                self.data_dict['description'] = instance.description
                self.data_dict['hostname'] = instance.hostname
                self.data_dict['enabled'] = instance.enabled
                break
        else:
            log_message = ('uid %s not found.') % (uid)
            log.log2die(1049, log_message)

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


class GetAgents(object):
    """Class to return agent data.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self):
        """Function for intializing the class.

        Args:
            uid: UID of agent

        Returns:
            None

        """
        # Initialize important variables
        self.data_dict = defaultdict(dict)
        self.agent_list = []
        # Prepare SQL query to read a record from the database.
        # Only active oids
        sql_query = (
            'SELECT '
            'iset_agent.idx, '
            'iset_agent.id, '
            'iset_agent.name, '
            'iset_agent.description, '
            'iset_agent.hostname, '
            'iset_agent.enabled, '
            'iset_agent.last_timestamp '
            'FROM iset_agent ')

        # Do query and get results
        database = db.Database()
        query_results = database.query(sql_query, 1038)
        # Massage data
        for row in query_results:
            # uid found?
            if not row[0]:
                log_message = ('uid %s not found.') % (uid)
                log.log2die(1049, log_message)

            # Assign values
            self.data_dict['idx'] = row[0]
            self.data_dict['id'] = row[1]
            self.data_dict['name'] = row[2]
            self.data_dict['description'] = row[3]
            self.data_dict['hostname'] = row[4]
            self.data_dict['enabled'] = row[5]
            self.data_dict['last_timestamp'] = row[6]
            local_dict = self.data_dict
            self.agent_list.append(local_dict.copy())

    def get_all(self):
        value = self.agent_list
        return value



class GetDataPoint(object):
    """Class to return agent data.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, idx):
        """Function for intializing the class.

        Args:
            idx: idx of agent

        Returns:
            None

        """
        # Initialize important variables
        self.data_point_dict = defaultdict(dict)
        self.idx = idx

        # Prepare SQL query to read a record from the database.
        # Only active oids
        sql_query = (
            'SELECT * '
            'FROM iset_datapoint '
            'WHERE '
            'idx_agent=\'%s\'') % (
                idx)

        # Do query and get results
        database = db.Database()
        query_results = list(database.query(sql_query, 1301))

        # Massage data
        for row in query_results:
            # uid found?
            if not idx:
                log_message = ('uid %s not found.') % (idx)
                jm_general.die(1050, log_message)
                # Assign values
            self.data_point_dict[row[3]] = [row[0], row[6]]

    def everything(self):
        """Get all datapoints.

        Args:
            None

        Returns:
            value: Dictionary of data_points

        """
        # Return
        value = self.data_point_dict
        return value
