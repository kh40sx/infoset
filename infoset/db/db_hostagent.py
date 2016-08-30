"""Module of infoset database functions.

Classes for agent data

"""
# Python standard libraries
from collections import defaultdict

# Python libraries
from sqlalchemy import and_

# Infoset libraries
from infoset.db import db
from infoset.db.db_orm import HostAgent
from infoset.utils import log


class GetHostAgent(object):
    """Class to return HostAgent data by host and agent idx.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, idx_host, idx_agent):
        """Method initializing the class.

        Args:
            idx_host: Host idx
            idx_agent: Agent idx

        Returns:
            None

        """
        # Initialize key variables
        self.data_dict = defaultdict(dict)

        # Establish a database session
        database = db.Database()
        session = database.session()
        result = session.query(HostAgent).filter(and_(
            HostAgent.idx_host == idx_host,
            HostAgent.idx_agent == idx_agent))

        # Massage data
        if result.count() == 1:
            for instance in result:
                self.data_dict['last_timestamp'] = instance.last_timestamp
                break
        else:
            log_message = (
                'Host IDX %s Agent IDX %s not found in iset_hostagent table.'
                '') % (idx_host, idx_agent)
            log.log2die(1105, log_message)

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


def host_agent_exists(idx_host, idx_agent):
    """Determine whether a host / agent entry exists in the HostAgent table.

    Args:
        idx_host: Host idx
        idx_agent: Agent idx

    Returns:
        found: True if found

    """
    # Initialize key variables
    found = False

    # Establish a database session
    database = db.Database()
    session = database.session()
    result = session.query(HostAgent.idx).filter(and_(
        HostAgent.idx_host == idx_host,
        HostAgent.idx_agent == idx_agent))

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


def host_indices(idx_agent):
    """Get list of all host indexes for a specific agent_idx.

    Args:
        None

    Returns:
        listing: List of indexes

    """
    idx_list = []

    # Establish a database session
    database = db.Database()
    session = database.session()
    result = session.query(HostAgent.idx_host).filter(
        HostAgent.idx_agent == idx_agent)
    session.close()

    # Add to the list of host idx values
    for instance in result:
        idx_list.append(instance.idx_host)

    # Return
    return idx_list


def agent_indices(idx_host):
    """Get list of all agent indexes for a specific host_idx.

    Args:
        None

    Returns:
        listing: List of indexes

    """
    idx_list = []

    # Establish a database session
    database = db.Database()
    session = database.session()
    result = session.query(HostAgent.idx_agent).filter(
        HostAgent.idx_host == idx_host)
    session.close()

    # Add to the list of host idx values
    for instance in result:
        idx_list.append(instance.idx_agent)

    # Return
    return idx_list
