"""Module of infoset database functions.

Classes for agent data

"""

# Python standard libraries
from collections import defaultdict

# Infoset libraries
from infoset.utils import log
from infoset.db import POOL
from infoset.db.db_orm import Datapoint


class GetSingleDataPoint(object):
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
            did: Datapoint id
            config: Config object

        Returns:
            None

        """
        # Initialize important variables
        self.data_dict = defaultdict(dict)

        # Establish a database session
        session = POOL()
        query = session.query(Datapoint).filter(Datapoint.idx == idx)

        # Massage data
        if query.count() == 1:
            for instance in query:
                self.data_dict['idx'] = instance.idx
                self.data_dict['id'] = instance.id
                self.data_dict['idx_agent'] = instance.idx_agent
                self.data_dict['agent_label'] = instance.agent_label
                self.data_dict['agent_source'] = instance.agent_source
                self.data_dict['enabled'] = instance.enabled
                self.data_dict['base_type'] = instance.base_type
                self.data_dict['multiplier'] = instance.multiplier
                self.data_dict['last_timestamp'] = instance.last_timestamp
                break
        else:
            log_message = ('Datapoint idx %s not found.') % (idx)
            log.log2die(1047, log_message)

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

    def __init__(self, idx):
        """Function for intializing the class.

        Args:
            idx: Datapoint Index

        Returns:
            None

        """
        # Initialize important variables
        self.data_dict = defaultdict(dict)

        # Establish a database session
        session = POOL()
        query = session.query(Datapoint).filter(Datapoint.idx == idx)

        # Massage data
        if query.count() == 1:
            for instance in query:
                self.data_dict['idx'] = instance.idx
                self.data_dict['id'] = instance.id
                self.data_dict['idx_agent'] = instance.idx_agent
                self.data_dict['agent_label'] = instance.agent_label
                self.data_dict['agent_source'] = instance.agent_source
                self.data_dict['enabled'] = instance.enabled
                self.data_dict['base_type'] = instance.base_type
                self.data_dict['multiplier'] = instance.multiplier
                self.data_dict['last_timestamp'] = instance.last_timestamp
                break
        else:
            log_message = ('idx %s not found.') % (idx)
            log.log2die(1048, log_message)

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
