#!/usr/bin/env python3
"""Infoset ORM classes.

Manages connection pooling among other things.

"""

# Infoset libraries
from infoset.utils import jm_general
from infoset.db.db_orm import OID
from infoset.db import db_oid
from infoset.db import db


def insert_oids(directory=None):
    """Update the database with certain key data.

    Args:
        directory: Directory to add to list

    Returns:
        None

    """
    # Initialize key variables
    root_dir = jm_general.root_directory()
    oids_directories = [('%s/infoset/metadata/oids') % (root_dir)]

    # Create a list of existing agent labels, that are unique by definition
    agent_labels = []
    all_oids = db_oid.all_oids()
    for item in all_oids:
        agent_labels.append(item['agent_label'])

    # Add directory to the search path if required
    if directory is not None:
        if os.path.isdir(directory) is True:
            oids_directories.extend(directory)

    # Read in the oid data
    oids_yaml = jm_general.read_yaml_files(oids_directories)

    # Get a list of all labels
    for item in oids_yaml:
        oid_values = item['oid_values']
        oid_labels = item['oid_labels']
        agent_label = item['agent_label']
        base_type = item['base_type']
        multiplier = item['multiplier']

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
