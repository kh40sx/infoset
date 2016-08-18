#!/usr/bin/env python3
"""Infoset ingest cache daemon.

Extracts agent data from cache directory files.

"""

# Standard libraries
import os
from pprint import pprint

# Infoset libraries
from infoset.utils import jm_configuration
from infoset.db import db_oid
from infoset.snmp import snmp_manager


def main():
    """Process agent data.

    Args:
        None

    Returns:
        None

    """
    # Process Cache
    agent_name = 'snmp'

    # Get configuration
    config_dir = os.environ['INFOSET_CONFIGDIR']
    config = jm_configuration.ConfigAgent(
        config_dir, agent_name)

    # Get hosts
    hostnames = config.agent_hostnames()

    # Get OIDs
    oids = db_oid.all_oids()

    pprint(hostnames)
    pprint(oids)

    # Process each hostname
    for hostname in hostnames:
        # Get SNMP information
        snmp_config = jm_configuration.ConfigSNMP(config_dir)
        validate = snmp_manager.Validate(hostname, snmp_config.snmp_auth())
        snmp_params = validate.credentials()

        # Check SNMP supported
        if snmp_params:
            snmp_object = snmp_manager.Interact(snmp_params)

            # Check support for each OID
            for item in oids:
                # Insert into iset_hostoid table if necessary
                if snmp_object.oid_exists(item['oid_values']) is True:
                    print('hooray', item['oid_values'])


if __name__ == "__main__":
    main()
