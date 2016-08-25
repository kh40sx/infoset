"""Module of infoset database functions.

Classes for agent data

"""

# Python standard libraries
from collections import defaultdict

# Infoset libraries
from infoset.utils import log
from infoset.utils import jm_general
from infoset.db import db
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
        database = db.Database()
        session = database.session()
        result = session.query(Datapoint).filter(Datapoint.idx == idx)

        # Massage data
        if result.count() == 1:
            for instance in result:
                self.data_dict['idx'] = instance.idx
                self.data_dict['id'] = instance.id
                self.data_dict['idx_agent'] = instance.idx_agent
                self.data_dict['idx_host'] = instance.idx_host
                self.data_dict[
                    'agent_label'] = jm_general.decode(instance.agent_label)
                self.data_dict[
                    'agent_source'] = jm_general.decode(instance.agent_source)
                self.data_dict['enabled'] = instance.enabled
                self.data_dict['uncharted_value'] = instance.uncharted_value
                self.data_dict['base_type'] = instance.base_type
                self.data_dict['last_timestamp'] = instance.last_timestamp
                break
        else:
            log_message = ('Datapoint idx %s not found.') % (idx)
            log.log2die(1047, log_message)

        # Return the session to the database pool after processing
        session.close()

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

        # Return the session to the database pool after processing
        session.close()

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

        # Return the session to the database pool after processing
        session.close()

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

    # Massage data
    if result.count() == 1:
        for instance in result:
            _ = instance.id
            break
        found = True

    # Return the session to the database pool after processing
    session.close()

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

    # Massage data
    if result.count() == 1:
        for instance in result:
            _ = instance.idx
            break
        found = True

    # Return the session to the database pool after processing
    session.close()

    # Return
    return found


def datapoint_indices(idx_host):
    """Get list of all datapoint indexes for a specific host_idx.

    Args:
        None

    Returns:
        listing: List of indexes

    """
    idx_list = []

    # Establish a database session
    database = db.Database()
    session = database.session()
    result = session.query(Datapoint.idx_host).filter(
        Datapoint.idx_host == idx_host)
    session.close()

    # Add to the list of host idx values
    for instance in result:
        idx_list.append(instance.idx_agent)

    # Return
    return idx_list
