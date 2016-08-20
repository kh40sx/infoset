#!/usr/bin/env python3
"""Infoset ORM classes.

Manages connection pooling among other things.

"""

# Main python libraries
import os
from pathlib import Path
from sqlalchemy import create_engine

# Infoset libraries
from infoset.utils import log
from infoset.utils import jm_configuration
from infoset.utils import jm_general
import infoset.utils
from infoset.db.db_orm import BASE, OID
from infoset.db import DBURL
from infoset.db import db_oid
from infoset.db import db


def main():
    """Process agent data.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    use_mysql = True
    pool_size = 25
    max_overflow = 25

    # Get configuration
    config_directory = os.environ['INFOSET_CONFIGDIR']
    config = jm_configuration.ConfigServer(config_directory)

    # Create DB connection pool
    if use_mysql is True:
        # Add MySQL to the pool
        engine = create_engine(
            DBURL, echo=True,
            encoding='utf8',
            max_overflow=max_overflow,
            pool_size=pool_size, pool_recycle=3600)

        # Try to create the database
        print('Attempting to create database tables')
        try:
            sql_string = (
                'ALTER DATABASE %s CHARACTER SET utf8mb4 '
                'COLLATE utf8mb4_general_ci') % (config.db_name())
            engine.execute(sql_string)
        except:
            log_message = (
                'Cannot connect to database %s. '
                'Verify database server is started. '
                'Verify database is created. '
                'Verify that the configured database authentication '
                'is correct.') % (config.db_name())
            log.log2die(1036, log_message)

        # Apply schemas
        print('Applying Schemas')
        BASE.metadata.create_all(engine)

        # Insert an entry for the infoset agent
        try:
            sql_string = (
                'INSERT INTO iset_agent (id, name, hostname) VALUES '
                '("_infoset", "_infoset", "_infoset")')
            engine.execute(sql_string)
        except:
            pass

        # Try some additional statements
        insert_oids()

    # Install required PIP packages
    print('Installing required pip3 packages')
    pip3 = infoset.utils.jm_general.search_file('pip3')
    if pip3 is None:
        log_message = ('Cannot find python "pip3". Please install.')
        log.log2die(1052, log_message)

    utils_directory = infoset.utils.__path__[0]
    requirements_file = ('%s/requirements.txt') % (
        Path(utils_directory).parents[1])
    script_name = (
        'pip3 install --user --requirement %s') % (requirements_file)
    infoset.utils.jm_general.run_script(script_name)


def insert_oids():
    """Update the database with certain key data.

    Args:
        None

    Returns:
        None

    """
    # Create a list of existing agent labels, that are unique by definition
    agent_labels = []
    all_oids = db_oid.all_oids()
    for item in all_oids:
        agent_labels.append(item['agent_label'])

    # Define a list of OIDs we need to add
    oid_data = [
        ('.1.3.6.1.4.1.1718.3.2.2.1.12', '.1.3.6.1.4.1.1718.3.2.2.1.3', 'Sentry3_infeedPower', 1, 1),
        ('.1.3.6.1.4.1.1718.3.2.2.1.7', '.1.3.6.1.4.1.1718.3.2.2.1.3', 'Sentry3_infeedLoadValue', 1, 0.01),
        ('.1.3.6.1.2.1.31.1.1.1.10', '.1.3.6.1.2.1.31.1.1.1.1', 'ifHCOutOctets', 64, 8),
        ('.1.3.6.1.2.1.31.1.1.1.6', '.1.3.6.1.2.1.31.1.1.1.1', 'ifHCInOctets', 64, 8)
    ]

    # Insert data if it doesn't already exist
    for line in oid_data:
        (oid_values, oid_labels, agent_label, base_type, multiplier) = line

        if db_oid.oid_values_exists(oid_values) is False:
            if agent_label not in agent_labels:
                # Prepare SQL query to read a record from the database.
                record = OID(
                    oid_values=jm_general.encode(oid_values),
                    oid_labels=jm_general.encode(oid_labels),
                    agent_label=jm_general.encode(agent_label),
                    base_type=base_type,
                    multiplier=multiplier)
                database = db.Database()
                database.add(record, 1091)


if __name__ == '__main__':
    main()
