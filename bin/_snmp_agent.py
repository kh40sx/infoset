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
from infoset.db import db_oid
from infoset.db import db_host
from infoset.db import db_hostoid
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

    # Get configuration
    config_dir = os.environ['INFOSET_CONFIGDIR']
    config = jm_configuration.ConfigAgent(
        config_dir, agent_name)

    # Get hosts
    hostnames = config.agent_hostnames()

    # Process each hostname
    for hostname in hostnames:
        # Get all oid IDX values tied to the hostname
        master = _master(hostname)

        # Get SNMP information
        snmp_config = jm_configuration.ConfigSNMP(config_dir)
        validate = snmp_manager.Validate(hostname, snmp_config.snmp_auth())
        snmp_params = validate.credentials()

        # Check SNMP supported
        if bool(snmp_params) is True:
            # Get datapoints
            _datapoints(snmp_params, master)


def _datapoints(snmp_params, master):
    """Create the master dictionary for the host.

    Args:
        labels_oid: OID used for labels
        oid: OID value

    Returns:
        value: Index value

    """
    # Get sources
    snmp_object = snmp_manager.Interact(snmp_params)
    for labels_oid in master.keys():
        sources = {}
        oid_results = snmp_object.swalk(labels_oid)
        for key, value in oid_results.items():
            sources[_index(labels_oid, key)] = jm_general.decode(value)

    # Get values
    for labels_oid in master.keys():
        # Initialize datapoints
        datapoints = defaultdict(lambda: defaultdict(dict))

        for agent_label in master[labels_oid].keys():
            # Information about the OID
            values_oid = master[labels_oid][agent_label]['values_oid']
            base_type = master[labels_oid][agent_label]['base_type']
            chartable = master[labels_oid][agent_label]['chartable']

            # Get OID values
            values = {}
            oid_results = snmp_object.swalk(values_oid)
            for key, value in oid_results.items():
                values[_index(labels_oid, key)] = value

            # Create list of data for json
            data = []
            for index, value in values.items():
                data.append([index, value, sources[index]])

            # Finish up dict for json
            datapoints[agent_label]['data'] = data
            datapoints[agent_label]['description'] = None
            datapoints[agent_label]['base_type'] = base_type

        pprint(master)
        print('\n')
        pprint(datapoints)


def _master(hostname):
    """Create the master dictionary for the host.

    Args:
        labels_oid: OID used for labels
        oid: OID value

    Returns:
        value: Index value

    """
    # Initialize key variables
    master = defaultdict(lambda: defaultdict(dict))

    # Get all oid IDX values tied to the hostname
    idx_host = db_host.GetHost(hostname).idx()
    oid_indices = db_hostoid.oid_indices(idx_host)

    # Get OID metadata
    for idx_oid in oid_indices:
        oid_object = db_oid.GetIDX(idx_oid)

        # Assign OIDs for values to the OID that
        # will be used to label the results
        labels_oid = oid_object.oid_labels()
        values_oid = oid_object.oid_values()
        agent_label = oid_object.agent_label()
        base_type = oid_object.base_type()
        chartable = oid_object.chartable()

        # Stuff to do
        if labels_oid not in master:
            master[labels_oid][agent_label]['values_oid'] = values_oid
            master[labels_oid][agent_label]['base_type'] = base_type
            master[labels_oid][agent_label]['chartable'] = chartable

    # Return
    return master


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
