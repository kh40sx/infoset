"""Module of infoset database functions.

Classes for agent data

"""
# Python libraries
from sqlalchemy import and_

# Infoset libraries
from infoset.db import db
from infoset.db.db_orm import HostAgent


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
        idx_host=idx_host, idx_agent=idx_agent))

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
