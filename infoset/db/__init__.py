#!/usr/bin/env python3
"""Infoset ORM classes.

Manages connection pooling among other things.

"""

# Main python libraries
import os
from sqlalchemy import create_engine

# Infoset libraries
from infoset.utils import jm_configuration
from infoset.utils import log
from infoset.db import db_orm

#############################################################################
# Setup a global pool for database connections
#############################################################################
POOL = None


def main():
    """Process agent data.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    global POOL

    # Get configuration
    log.check_environment()

    config_directory = os.environ['INFOSET_CONFIGDIR']
    config = jm_configuration.ConfigServer(config_directory)

    # Create DB connection pool
    db_uri = ('mysql+pymysql://%s:%s@%s/%s') % (
        config.db_username(), config.db_password(),
        config.db_hostname(), config.db_name())
    POOL = create_engine(db_uri, echo=False)


if __name__ == 'infoset.db':
    main()
