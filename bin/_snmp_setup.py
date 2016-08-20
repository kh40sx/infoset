#!/usr/bin/env python3
"""Infoset ingest cache daemon.

Extracts agent data from cache directory files.

"""

# Standard libraries
import os
from pprint import pprint

# Infoset libraries
from infoset.utils import jm_configuration
from infoset.utils import jm_general
from infoset.db import db
from infoset.db import db_oid
from infoset.db import db_host
from infoset.db import db_hostoid
from infoset.db.db_orm import HostOID, Host
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
        if bool(snmp_params) is True:
            snmp_object = snmp_manager.Interact(snmp_params)

            # Check support for each OID
            for item in oids:
                # Get oid
                oid = item['oid_values']

                # Actions must be taken if a valid OID is found
                if snmp_object.oid_exists(oid) is True:
                    # Insert into iset_hostoid table if necessary
                    if db_host.hostname_exists(hostname) is False:
                        record = Host(
                            hostname=jm_general.encode(hostname),
                            snmp_enabled=1)
                        database = db.Database()
                        database.add(record, 1089)

                    # Get idx for host and oid
                    idx_host = db_host.GetHost(hostname).idx()
                    idx_oid = item['idx']

                    # Insert an entry in the HostOID table if required
                    if db_hostoid.host_oid_exists(idx_host, idx_oid) is False:
                        # Prepare SQL query to read a record from the database.
                        record = HostOID(idx_host=idx_host, idx_oid=idx_oid)
                        database = db.Database()
                        database.add(record, 1090)

                        print('Inserted!', hostname, idx_host, idx_oid)


if __name__ == "__main__":
    main()
