"""Module of infoset database functions.

Classes for agent data

"""

# Python standard libraries
from collections import defaultdict

# PIP libraries
from sqlalchemy import and_

# Infoset libraries
from infoset.utils import log
from infoset.utils import jm_general
from infoset.db import db
from infoset.db.db_orm import Datapoint


class GetDID(object):
    """Class to return datapoint data by datapoint idx.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, did):
        """Function for intializing the class.

        Args:
            did: Datapoint ID

        Returns:
            None

        """
        # Initialize important variables
        self.data_dict = defaultdict(dict)
        value = did.encode()

        # Establish a database session
        database = db.Database()
        session = database.session()
        result = session.query(Datapoint).filter(Datapoint.id == value)

        # Return the session to the database pool after processing
        database.close()

        # Massage data
        if result.count() == 1:
            for instance in result:
                self.data_dict['idx'] = instance.idx
                self.data_dict['id'] = instance.id
                self.data_dict['idx_agent'] = instance.idx_agent
                self.data_dict['idx_host'] = instance.idx_host
                self.data_dict['idx_department'] = instance.idx_department
                self.data_dict['idx_billtype'] = instance.idx_billtype
                self.data_dict[
                    'agent_label'] = jm_general.decode(instance.agent_label)
                self.data_dict[
                    'agent_source'] = jm_general.decode(instance.agent_source)
                self.data_dict['enabled'] = instance.enabled
                self.data_dict['billable'] = instance.billable
                self.data_dict[
                    'base_type'] = jm_general.decode(instance.base_type)
                self.data_dict['uncharted_value'] = instance.uncharted_value
                self.data_dict['last_timestamp'] = instance.last_timestamp
                break
        else:
            log_message = ('did %s not found.') % (did)
            log.log2die(1085, log_message)

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

    def uncharted_value(self):
        """Get uncharted_value value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['uncharted_value']
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

    def billable(self):
        """Get billable value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['billable']
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

    def idx_host(self):
        """Get idx_host value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['idx_host']
        return value

    def idx_department(self):
        """Get idx_department value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['idx_department']
        return value

    def idx_billtype(self):
        """Get idx_billtype value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['idx_billtype']
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
    """Class to return datapoint data by datapoint idx.

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
        database = db.Database()
        session = database.session()
        result = session.query(Datapoint).filter(Datapoint.idx == idx)

        # Return the session to the database pool after processing
        database.close()

        # Massage data
        if result.count() == 1:
            for instance in result:
                self.data_dict['idx'] = instance.idx
                self.data_dict['id'] = jm_general.decode(instance.id)
                self.data_dict['idx_agent'] = instance.idx_agent
                self.data_dict['idx_host'] = instance.idx_host
                self.data_dict['idx_department'] = instance.idx_department
                self.data_dict['idx_billtype'] = instance.idx_billtype
                self.data_dict[
                    'agent_label'] = jm_general.decode(instance.agent_label)
                self.data_dict[
                    'agent_source'] = jm_general.decode(instance.agent_source)
                self.data_dict['enabled'] = instance.enabled
                self.data_dict['billable'] = instance.billable
                self.data_dict['base_type'] = instance.base_type
                self.data_dict['uncharted_value'] = instance.uncharted_value
                self.data_dict['last_timestamp'] = instance.last_timestamp
                break
        else:
            log_message = ('idx %s not found.') % (idx)
            log.log2die(1084, log_message)

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

    def uncharted_value(self):
        """Get uncharted_value value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['uncharted_value']
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

    def billable(self):
        """Get billable value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['billable']
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

    def idx_host(self):
        """Get idx_host value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['idx_host']
        return value

    def idx_department(self):
        """Get idx_department value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['idx_department']
        return value

    def idx_billtype(self):
        """Get idx_billtype value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['idx_billtype']
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


def did_exists(did):
    """Determine whether the DID exists.

    Args:
        did: DID value for datapoint

    Returns:
        found: True if found

    """
    # Initialize key variables
    found = False
    value = did.encode()

    # Establish a database session
    database = db.Database()
    session = database.session()
    result = session.query(Datapoint.id).filter(Datapoint.id == value)

    # Return the session to the database pool after processing
    database.close()

    # Massage data
    if result.count() == 1:
        for instance in result:
            _ = instance.id
            break
        found = True

    # Return
    return found


def idx_exists(idx):
    """Determine whether the idx exists.

    Args:
        idx: idx value for datapoint

    Returns:
        found: True if found

    """
    # Initialize key variables
    found = False

    # Establish a database session
    database = db.Database()
    session = database.session()
    result = session.query(Datapoint.idx).filter(Datapoint.idx == idx)

    # Return the session to the database pool after processing
    database.close()

    # Massage data
    if result.count() == 1:
        for instance in result:
            _ = instance.idx
            break
        found = True

    # Return
    return found


def datapoint_host_idx(idx_host):
    """Get list of all datapoint indexes for a specific host_idx.

    Args:
        idx_host: Host index

    Returns:
        listing: List of indexes

    """
    # Initialize key variables
    idx_list = []

    # Establish a database session
    database = db.Database()
    session = database.session()
    result = session.query(Datapoint.idx).filter(
        Datapoint.idx_host == idx_host)
    database.close()

    # Add to the list of host idx values
    for instance in result:
        idx_list.append(instance.idx)

    # Return
    return idx_list


def datapoint_host_agent(idx_host, idx_agent):
    """List of datapoint data for a specific host_idx, idx_agent combination.

    Args:
        idx_host: Host index
        idx_agent: Agent index

    Returns:
        dict_list: List of dicts containing data

    """
    # Initialize key variables
    dict_list = []

    # Establish a database session
    database = db.Database()
    session = database.session()
    result = session.query(Datapoint).filter(
        and_(
            Datapoint.uncharted_value == None,
            Datapoint.idx_host == idx_host,
            Datapoint.idx_agent == idx_agent)
        )
    database.close()

    # Add to the list of host idx values
    for instance in result:
        data_dict = {}
        data_dict['idx'] = instance.idx
        data_dict['id'] = jm_general.decode(instance.id)
        data_dict['idx_agent'] = instance.idx_agent
        data_dict['idx_host'] = instance.idx_host
        data_dict['idx_department'] = instance.idx_department
        data_dict['idx_billtype'] = instance.idx_billtype
        data_dict[
            'agent_label'] = jm_general.decode(instance.agent_label)
        data_dict[
            'agent_source'] = jm_general.decode(instance.agent_source)
        data_dict['enabled'] = bool(instance.enabled)
        data_dict['billable'] = bool(instance.billable)
        data_dict['base_type'] = instance.base_type
        data_dict['uncharted_value'] = instance.uncharted_value
        data_dict['last_timestamp'] = instance.last_timestamp
        dict_list.append(data_dict)

    # Return
    return dict_list
