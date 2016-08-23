"""Module of infoset database functions.

Classes for agent data

"""

# Python standard libraries
from collections import defaultdict

# Infoset libraries
from infoset.utils import log
from infoset.utils import jm_general
from infoset.db import db
from infoset.db.db_orm import BillType


class GetCode(object):
    """Class to return BillType data by code.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, code):
        """Function for intializing the class.

        Args:
            code: BillType code

        Returns:
            None

        """
        # Initialize important variables
        self.data_dict = defaultdict(dict)
        value = code.encode()

        # Establish a database session
        database = db.Database()
        session = database.session()
        result = session.query(BillType).filter(BillType.code == value)

        # Massage data
        if result.count() == 1:
            for instance in result:
                self.data_dict['idx'] = instance.idx
                self.data_dict[
                    'code'] = jm_general.decode(instance.code)
                self.data_dict[
                    'name'] = jm_general.decode(instance.name)
                break
        else:
            log_message = ('BillType %s not found.') % (code)
            log.log2die(1001, log_message)

        # Return the session to the database pool after processing
        session.close()

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

    def code(self):
        """Get code value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['code']
        return value

    def name(self):
        """Get name value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['name']
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
            idx: BillType Index

        Returns:
            None

        """
        # Initialize important variables
        self.data_dict = defaultdict(dict)

        # Establish a database session
        database = db.Database()
        session = database.session()
        result = session.query(BillType).filter(BillType.idx == idx)

        # Massage data
        if result.count() == 1:
            for instance in result:
                self.data_dict['idx'] = instance.idx
                self.data_dict[
                    'code'] = jm_general.decode(instance.code)
                self.data_dict[
                    'name'] = jm_general.decode(instance.name)
                break
        else:
            log_message = ('BillType idx %s not found.') % (idx)
            log.log2die(1099, log_message)

        # Return the session to the database pool after processing
        session.close()

    def code(self):
        """Get code value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['code']
        return value

    def name(self):
        """Get name value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['name']
        return value


def code_exists(code):
    """Determine whether the code exists.

    Args:
        code: BillType code

    Returns:
        found: True if found

    """
    # Initialize key variables
    found = False
    value = code.encode()

    # Establish a database session
    database = db.Database()
    session = database.session()
    result = session.query(BillType.code).filter(BillType.code == value)

    # Massage data
    if result.count() == 1:
        for instance in result:
            _ = instance.code
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
    result = session.query(BillType.idx).filter(BillType.idx == idx)

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
