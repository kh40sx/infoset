#!/usr/bin/env python3
"""Classes for polling remote hosts for SNMP data."""

import os
import yaml


import jm_general


class File(object):
    """Process configuration file for a host.

    The aim of this class is to process the YAML file consistently
    across multiple manufacturers and present it to other classes
    consistently. That way manufacturer specific code for processing YAML
    data is in one place.

    """

    def __init__(self, config, host):
        """Initialize class.

        Args:
            config: Configuration file object
            host: Hostname to process

        Returns:
            data_dict: Dict of summary data

        """
        # Initialize key variables
        self.ports = {}
        yaml_file = ('%s/%s.yaml') % (config.snmp_directory(), host)

        # Fail if yaml file doesn't exist
        if os.path.isfile(yaml_file) is False:
            log_message = (
                'YAML file %s for host %s doesn\'t exist! '
                'Try polling devices first.') % (yaml_file, host)
            jm_general.logit(1017, log_message, False)

        # Read file
        with open(yaml_file, 'r') as file_handle:
            yaml_from_file = file_handle.read()
        yaml_data = yaml.load(yaml_from_file)

        # Create dict for layer1 Ethernet data
        for key, metadata in yaml_data['layer1'].items():
            if _is_ethernet(metadata) is True:
                self.ports[int(key)] = metadata

        # Get system
        self.system = yaml_data['system']

    def system_summary(self):
        """Return system summary data.

        Args:
            None

        Returns:
            data_dict: Dict of summary data

        """
        # Initialize key variables
        data_dict = {}

        # Assign system variables
        v2mib = self.system['SNMPv2-MIB']
        for key in v2mib.keys():
            data_dict[key] = v2mib[key]['0']

        # Return
        return data_dict

    def ethernet_data(self):
        """Return L1 data for Ethernet ports only.

        Args:
            None

        Returns:
            self.ports: L1 data for Ethernet ports

        """
        return self.ports


def _is_ethernet(metadata):
    """Return whether ifIndex metadata belongs to an Ethernet port.

    Args:
        metadata: Data dict related to the port

    Returns:
        valid: True if valid ethernet port

    """
    # Initialize key variables
    valid = False

    # Process ifType
    if 'ifType' in metadata:
        # Get port name
        name = metadata['ifName'].lower()

        # Process ethernet ports
        if metadata['ifType'] == 6:
            # VLAN L2 VLAN interfaces passing as Ethernet
            if name.startswith('vl') is False:
                valid = True

    # Return
    return valid
