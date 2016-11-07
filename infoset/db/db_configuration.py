"""Module of infoset database functions.

Classes for agent data

"""

# Python standard libraries
from collections import defaultdict

# Infoset libraries
from infoset.utils import log
from infoset.utils import jm_general
from infoset.db import db
from infoset.db.db_orm import Configuration


class GetConfigurationKey(object):
    """Class to return Configuration data by config_key.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, config_key):
        """Function for intializing the class.

        Args:
            config_key: Configuration config_key

        Returns:
            None

        """
        # Initialize important variables
        self.data_dict = defaultdict(dict)
        value = config_key.encode()

        # Establish a database session
        database = db.Database()
        session = database.session()
        result = session.query(
            Configuration).filter(Configuration.config_key == value)

        # Return the session to the database pool after processing
        database.close()

        # Massage data
        if result.count() == 1:
            for instance in result:
                self.data_dict['idx'] = instance.idx
                self.data_dict[
                    'config_key'] = jm_general.decode(instance.config_key)
                self.data_dict[
                    'name'] = jm_general.decode(instance.name)
                break
        else:
            log_message = ('Configuration %s not found.') % (config_key)
            log.log2die(1048, log_message)

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

    def config_key(self):
        """Get config_key value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['config_key']
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
            idx: Configuration Index

        Returns:
            None

        """
        # Initialize important variables
        self.data_dict = defaultdict(dict)

        # Establish a database session
        database = db.Database()
        session = database.session()
        result = session.query(Configuration).filter(Configuration.idx == idx)

        # Return the session to the database pool after processing
        database.close()

        # Massage data
        if result.count() == 1:
            for instance in result:
                self.data_dict['idx'] = instance.idx
                self.data_dict[
                    'config_key'] = jm_general.decode(instance.config_key)
                self.data_dict[
                    'name'] = jm_general.decode(instance.name)
                break
        else:
            log_message = ('Configuration idx %s not found.') % (idx)
            log.log2die(1086, log_message)

    def config_key(self):
        """Get config_key value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['config_key']
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


def config_key_exists(config_key):
    """Determine whether the config_key exists.

    Args:
        config_key: Configuration config_key

    Returns:
        found: True if found

    """
    # Initialize key variables
    found = False
    value = config_key.encode()

    # Establish a database session
    database = db.Database()
    session = database.session()
    result = session.query(
        Configuration.config_key).filter(Configuration.config_key == value)

    # Return the session to the database pool after processing
    database.close()

    # Massage data
    if result.count() == 1:
        for instance in result:
            _ = instance.config_key
            break
        found = True

    # Return
    return found
