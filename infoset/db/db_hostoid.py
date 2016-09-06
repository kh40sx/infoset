"""Module of infoset database functions.

Classes for oid data

"""
# Python libraries
from sqlalchemy import and_

# Infoset libraries
from infoset.db import db
from infoset.db.db_orm import HostOID


def host_oid_exists(idx_host, idx_oid):
    """Determine whether a host / oid entry exists in the HostOID table.

    Args:
        idx_host: Host idx
        idx_oid: Agent idx

    Returns:
        found: True if found

    """
    # Initialize key variables
    found = False

    # Establish a database session
    database = db.Database()
    session = database.session()
    result = session.query(HostOID.idx).filter(and_(
        HostOID.idx_host == idx_host,
        HostOID.idx_oid == idx_oid))

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


def host_indices(idx_oid):
    """Get list of all host indexes for a specific oid_idx.

    Args:
        idx_oid: idx for oid

    Returns:
        idx_list: List of indexes

    """
    idx_list = []

    # Establish a database session
    database = db.Database()
    session = database.session()
    result = session.query(HostOID.idx_host).filter(
        HostOID.idx_oid == idx_oid)
    session.close()

    # Add to the list of host idx values
    for instance in result:
        idx_list.append(instance.idx_host)

    # Return
    return idx_list


def oid_indices(idx_host):
    """Get list of all oid indexes for a specific host_idx.

    Args:
        idx_host: idx for host

    Returns:
        idx_list: List of indexes

    """
    idx_list = []

    # Establish a database session
    database = db.Database()
    session = database.session()
    result = session.query(HostOID.idx_oid).filter(
        HostOID.idx_host == idx_host)
    session.close()

    # Add to the list of host idx values
    for instance in result:
        idx_list.append(instance.idx_oid)

    # Return
    return idx_list
