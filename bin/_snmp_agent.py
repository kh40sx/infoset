#!/usr/bin/env python3
"""Infoset ingest cache daemon.

Extracts agent data from cache directory files.

"""

# Standard libraries
import os
from collections import defaultdict
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
    # Initialize key variables
    agent_name = 'snmp'
    master = defaultdict(lambda: defaultdict(dict))
    data = defaultdict(lambda: defaultdict(dict))

    # Get configuration
    config_dir = os.environ['INFOSET_CONFIGDIR']
    config = jm_configuration.ConfigAgent(
        config_dir, agent_name)

    # Get hosts
    hostnames = config.agent_hostnames()

    # Process each hostname
    for hostname in hostnames:
        # Get all oid IDX values tied to the hostname
        idx_host = db_host.GetHost(hostname).idx()
        oid_indices = db_hostoid.oid_indices(idx_host)
        print(oid_indices)

        for idx_oid in oid_indices:
            oid_object = db_oid.GetIDX(idx_oid)

            # Assign OIDs for values to the OID that
            # will be used to label the results
            labels_oid = oid_object.oid_labels()
            values_oid = oid_object.oid_values()
            agent_label = oid_object.agent_label()
            if labels_oid in master:
                master[labels_oid]['values'].append(values_oid)
                master[labels_oid]['agent_label'].append(agent_label)
            else:
                master[labels_oid]['values'] = [values_oid]
                master[labels_oid]['agent_label'] = [agent_label]

        # Get SNMP information
        snmp_config = jm_configuration.ConfigSNMP(config_dir)
        validate = snmp_manager.Validate(hostname, snmp_config.snmp_auth())
        snmp_params = validate.credentials()

        # Check SNMP supported
        if bool(snmp_params) is True:
            # Get labels
            snmp_object = snmp_manager.Interact(snmp_params)
            for labels_oid in master.keys():
                data_dict = {}
                oid_results = snmp_object.swalk(labels_oid)
                for key, value in oid_results.items():
                    data_dict[_index(labels_oid, key)] = value
                master[labels_oid]['labels'] = data_dict

            # Get values
            for key in master.keys():
                for oid_value in master[key]['values']:
                    data_dict = {}
                    oid_results = snmp_object.swalk(oid_value)
                    for key, value in oid_results.items():
                        data_dict[_index(labels_oid, key)] = value
                    master[labels_oid]['labels'] = data_dict


                    print(peter)

        print(hostname)
        pprint(master)
        print('\n')

        """
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
                        record = Host(hostname=hostname, snmp_enabled=1)
                        database = db.Database()
                        database.add(record, 1081)

                    # Get idx for host and oid
                    idx_host = db_host.GetHost(hostname).idx()
                    idx_oid = item['idx']

                    # Insert an entry in the HostOID table if required
                    if db_hostoid.host_oid_exists(idx_host, idx_oid) is False:
                        # Prepare SQL query to read a record from the database.
                        record = HostOID(idx_host=idx_host, idx_oid=idx_oid)
                        database = db.Database()
                        database.add(record, 1081)

                        print('Inserted!', hostname, idx_host, idx_oid)
        """


def _index(labels_oid, oid):
    """Find the index value of an OID.

    Args:
        labels_oid: OID used for labels
        oid: OID value

    Returns:
        value: Index value

    """
    # Initialize key variables
    value = None

    # Get all the nodes in the oids
    nodes_label = labels_oid.split('.')
    nodes_oid = oid.split('.')

    # Calculate the difference in lenth in terms of OID nodes
    nodes_in_index = len(nodes_oid) - len(nodes_label)

    # Calculate what the index should be
    value_nodes = nodes_oid[-nodes_in_index:]
    if nodes_in_index == 1:
        value = int(value_nodes[0])
    else:
        value = '.'.join(value_nodes)

    # Return
    return value


if __name__ == "__main__":
    main()
