"""Module of infoset database functions.

Classes for agent data

"""

# Python standard libraries
from collections import defaultdict

# PIP Python libraries
from sqlalchemy import and_

# Infoset libraries
from infoset.utils import log
from infoset.utils import jm_general
from infoset.db import db
from infoset.db.db_orm import Host


class GetHost(object):
    """Class to return host data by hostname.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, hostname):
        """Function for intializing the class.

        Args:
            hostname: Hostname

        Returns:
            None

        """
        # Initialize important variables
        self.data_dict = defaultdict(dict)
        value = str(hostname).encode()

        # Establish a database session
        database = db.Database()
        session = database.session()
        result = session.query(Host).filter(Host.hostname == value)

        # Return the session to the database pool after processing
        database.close()

        # Massage data
        if result.count() == 1:
            for instance in result:
                self.data_dict['idx'] = instance.idx
                self.data_dict[
                    'hostname'] = jm_general.decode(instance.hostname)
                self.data_dict[
                    'description'] = jm_general.decode(instance.description)
                self.data_dict['enabled'] = instance.enabled
                self.data_dict['snmp_enabled'] = instance.snmp_enabled
                self.data_dict[
                    'ip_address'] = jm_general.decode(instance.ip_address)
                break
        else:
            log_message = ('Hostname %s not found.') % (hostname)
            log.log2die(1000, log_message)

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

    def hostname(self):
        """Get hostname value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['hostname']
        return value

    def description(self):
        """Get description value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['description']
        return value

    def enabled(self):
        """Get enabled value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = bool(self.data_dict['enabled'])
        return value

    def ip_address(self):
        """Get ip_address value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['ip_address']
        return value

    def snmp_enabled(self):
        """Get snmp_enabled value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = bool(self.data_dict['snmp_enabled'])
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
            idx: Host Index

        Returns:
            None

        """
        # Initialize important variables
        self.data_dict = defaultdict(dict)

        # Establish a database session
        database = db.Database()
        session = database.session()
        result = session.query(Host).filter(Host.idx == idx)

        # Return the session to the database pool after processing
        database.close()

        # Massage data
        if result.count() == 1:
            for instance in result:
                self.data_dict['idx'] = instance.idx
                self.data_dict[
                    'hostname'] = jm_general.decode(instance.hostname)
                self.data_dict[
                    'description'] = jm_general.decode(instance.description)
                self.data_dict['enabled'] = instance.enabled
                self.data_dict['snmp_enabled'] = instance.snmp_enabled
                self.data_dict[
                    'ip_address'] = jm_general.decode(instance.ip_address)
                break
        else:
            log_message = ('Host idx %s not found.') % (idx)
            log.log2die(1098, log_message)

    def hostname(self):
        """Get hostname value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['hostname']
        return value

    def description(self):
        """Get description value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['description']
        return value

    def enabled(self):
        """Get enabled value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = bool(self.data_dict['enabled'])
        return value

    def ip_address(self):
        """Get ip_address value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['ip_address']
        return value

    def snmp_enabled(self):
        """Get snmp_enabled value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = bool(self.data_dict['snmp_enabled'])
        return value


def all_hosts(enabled=True):
    """Get list of all hosts.

    Args:
        enabled: Only return enabled hosts if true

    Returns:
        hostlist: List of dicts of host data

    """
    hostlist = []
    idx_list = []

    # Establish a database session
    database = db.Database()
    session = database.session()
    if enabled is True:
        result = session.query(Host.idx).filter(Host.enabled == 1)
    else:
        result = session.query(Host.idx)
    database.close()

    # Add to the list of host idx values
    for instance in result:
        idx_list.append(instance.idx)

    # Get host information
    if bool(idx_list) is True:
        for idx in idx_list:
            data_dict = {}
            host = GetIDX(idx)
            data_dict['hostname'] = host.hostname()
            data_dict['description'] = host.description()
            data_dict['enabled'] = host.enabled()
            data_dict['snmp_enabled'] = host.enabled()
            data_dict['ip_address'] = host.ip_address()
            hostlist.append(data_dict)

    # Return
    return hostlist


def hostname_exists(hostname):
    """Determine whether the hostname exists.

    Args:
        hostname: Hostname

    Returns:
        found: True if found

    """
    # Initialize key variables
    found = False
    value = hostname.encode()

    # Establish a database session
    database = db.Database()
    session = database.session()
    result = session.query(Host.hostname).filter(Host.hostname == value)

    # Return the session to the database pool after processing
    database.close()

    # Massage data
    if result.count() == 1:
        for instance in result:
            _ = instance.hostname
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
    result = session.query(Host.idx).filter(Host.idx == idx)

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
