"""Module of infoset database functions.

Classes for agent data

"""

# Python standard libraries
from collections import defaultdict

# Infoset libraries
from infoset.utils import log
from infoset.utils import jm_general
from infoset.db import db
from infoset.db.db_orm import OID


class GetOID(object):
    """Class to return host data by oid_values.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, oid_values):
        """Function for intializing the class.

        Args:
            oid_values: OID

        Returns:
            None

        """
        # Initialize important variables
        self.data_dict = defaultdict(dict)

        # Establish a database session
        database = db.Database()
        session = database.session()
        result = session.query(OID).filter(OID.oid_values == oid_values)

        # Return the session to the database pool after processing
        database.close()

        # Massage data
        if result.count() == 1:
            for instance in result:
                self.data_dict['idx'] = instance.idx
                self.data_dict[
                    'oid_values'] = jm_general.decode(instance.oid_values)
                self.data_dict[
                    'oid_labels'] = jm_general.decode(instance.oid_labels)
                self.data_dict[
                    'agent_label'] = jm_general.decode(instance.agent_label)
                self.data_dict['base_type'] = instance.base_type
                self.data_dict['multiplier'] = instance.multiplier
                break
        else:
            log_message = ('OID %s not found.') % (oid_values)
            log.log2die(1040, log_message)

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

    def oid_values(self):
        """Get oid_values value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['oid_values']
        return value

    def oid_labels(self):
        """Get oid_labels value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['oid_labels']
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


class GetIDX(object):
    """Class to return host data by idx.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, idx):
        """Function for intializing the class.

        Args:
            idx: OID Index

        Returns:
            None

        """
        # Initialize important variables
        self.data_dict = defaultdict(dict)

        # Establish a database session
        database = db.Database()
        session = database.session()
        result = session.query(OID).filter(OID.idx == idx)

        # Return the session to the database pool after processing
        database.close()

        # Massage data
        if result.count() == 1:
            for instance in result:
                self.data_dict['idx'] = instance.idx
                self.data_dict[
                    'oid_values'] = jm_general.decode(instance.oid_values)
                self.data_dict[
                    'oid_labels'] = jm_general.decode(instance.oid_labels)
                self.data_dict[
                    'agent_label'] = jm_general.decode(instance.agent_label)
                self.data_dict['base_type'] = instance.base_type
                self.data_dict['multiplier'] = instance.multiplier
                break
        else:
            log_message = ('OID idx %s not found.') % (idx)
            log.log2die(1092, log_message)

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

    def oid_values(self):
        """Get oid_values value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['oid_values']
        return value

    def oid_labels(self):
        """Get oid_labels value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['oid_labels']
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


def all_oids():
    """Get list of all oids.

    Args:
        None

    Returns:
        hostlist: List of dicts of oids data

    """
    hostlist = []
    idx_list = []

    # Establish a database session
    database = db.Database()
    session = database.session()
    result = session.query(OID.idx)
    database.close()

    # Add to the list of host idx values
    for instance in result:
        idx_list.append(instance.idx)

    # Get host information
    if bool(idx_list) is True:
        for idx in idx_list:
            data_dict = {}
            host = GetIDX(idx)
            data_dict['idx'] = host.idx()
            data_dict['oid_values'] = host.oid_values()
            data_dict['oid_labels'] = host.oid_labels()
            data_dict['agent_label'] = host.agent_label()
            data_dict['base_type'] = host.base_type()
            data_dict['multiplier'] = host.multiplier()
            hostlist.append(data_dict)

    # Return
    return hostlist


def oid_values_exists(values):
    """Determine whether the oid_values exists.

    Args:
        values: OID

    Returns:
        found: True if found

    """
    # Initialize key variables
    found = False
    oid_values = values.encode()

    # Establish a database session
    database = db.Database()
    session = database.session()
    result = session.query(
        OID.oid_values).filter(OID.oid_values == oid_values)

    # Return the session to the database pool after processing
    database.close()

    # Massage data
    if result.count() == 1:
        for instance in result:
            _ = instance.oid_values
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
    result = session.query(OID.idx).filter(OID.idx == idx)

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
