#!/usr/bin/env python3
"""Infoset ORM classes.

Manages connection pooling among other things.

"""

# Main python libraries
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

# Infoset libraries
from infoset.utils import jm_configuration
from infoset.utils import log
from infoset.db import db_orm

#############################################################################
# Setup a global pool for database connections
#############################################################################
POOL = None


def connection_mysql():
    """Create a MySQL connection object to the database.

    Args:
        None

    Returns:
        connection: Connection object

    """
    # Initialize key variables
    return

    """
    config_directory = os.environ['INFOSET_CONFIGDIR']
    config = jm_configuration.ConfigServer(config_directory)

    # Create connection object
    connection = pymysql.connect(
        host=config.db_hostname(),
        user=config.db_username(),
        passwd=config.db_password(),
        db=config.db_name())

    # Return
    return connection
    """


def main():
    """Process agent data.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    use_mysql = True
    global POOL

    # Get configuration
    log.check_environment()

    config_directory = os.environ['INFOSET_CONFIGDIR']
    config = jm_configuration.ConfigServer(config_directory)

    # Create DB connection pool
    if use_mysql is True:
        db_uri = ('mysql+pymysql://%s:%s@%s/%s') % (
            config.db_username(), config.db_password(),
            config.db_hostname(), config.db_name())

        # Add MySQL to the pool
        db_engine = create_engine(db_uri, echo=False)
        POOL = scoped_session(
            sessionmaker(
                autoflush=True,
                autocommit=False,
                bind=db_engine
            )
        )

    else:
        POOL = None


if __name__ == 'infoset.db':
    main()
