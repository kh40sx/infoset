#!/usr/bin/env python3
"""Infoset ingest cache daemon.

Extracts agent data from cache directory files.

"""

# Standard libraries
import argparse
import textwrap

# Infoset libraries
from infoset.utils import jm_configuration
from infoset.utils import jm_general
from infoset.utils import log
from infoset.db import db
from infoset.db import db_oid
from infoset.db import db_host
from infoset.db import db_hostoid
from infoset.db.db_orm import HostOID, Host
from infoset.snmp import snmp_manager


def cli():
    """Return all the CLI options.

    Args:
        None

    Returns:
        args: Namespace() containing all of our CLI arguments as objects
            - filename: Path to the configuration file

    """
    # Header for the help menu of the application
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)

    # CLI argument for output filename
    parser.add_argument(
        '--hostname',
        required=True,
        type=str,
        help=textwrap.fill(
            'Individual hostname to evaluate. If not defined, '
            'the script will evaluate all hosts in the database, '
            'which could take some time. Use a hostname of "ALL" '
            'to evaluate all SNMP hosts in the system', width=80)
    )

    # Get the parser value
    args = parser.parse_args()

    # Return
    return args


def main():
    """Process agent data.

    Args:
        None

    Returns:
        None

    """
    # Process Cache
    agent_name = 'snmp'

    # Process CLI
    cli_args = cli()

    # Get configuration
    config = jm_configuration.ConfigAgent(agent_name)

    # Get hosts
    if cli_args.hostname.lower() == 'all':
        hostnames = config.agent_hostnames()
    else:
        # Check to make sure hostname exists in the configuration
        all_hosts = config.agent_hostnames()
        cli_hostname = cli_args.hostname
        if cli_hostname not in all_hosts:
            log_message = (
                'Agent "%s": Hostname %s is not present '
                'in the the configuration file.'
                '') % (agent_name, cli_hostname)
            log.log2die(1103, log_message)
        else:
            hostnames = [cli_hostname]

    # Get OIDs
    oids = db_oid.all_oids()

    # Process each hostname
    for hostname in hostnames:
        # Get SNMP information
        snmp_config = jm_configuration.ConfigSNMP()
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


if __name__ == "__main__":
    main()
