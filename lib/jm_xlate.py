#!/usr/bin/env python3
"""Classes for polling remote hosts for SNMP data."""

import os
import yaml
from pprint import pprint


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
                # Update duplex to universal infoset metadata value
                metadata['duplex'] = _duplex(metadata)
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


def _duplex(metadata):
    """Return duplex value for port.

    Args:
        metadata: Data dict related to the port

    Returns:
        duplex: Duplex value
            0) Unknown
            1) Half
            2) Full
            3) Half Auto
            4) Full Auto

    """
    # Initialize key variables
    duplex = 0

    # Process swPortDuplexStatus
    if 'swPortDuplexStatus' in metadata:
        value = metadata['swPortDuplexStatus']

        # Process duplex
        if value == 1:
            duplex = 2
        else:
            duplex = 1

    # Process dot3StatsDuplexStatus
    elif 'dot3StatsDuplexStatus' in metadata:
        value = metadata['dot3StatsDuplexStatus']

        # Process duplex
        if value == 2:
            duplex = 1
        elif value == 3:
            duplex = 2

    # Process portDuplex
    elif 'portDuplex' in metadata:
        value = metadata['portDuplex']

        # Process duplex
        if value == 1:
            duplex = 1
        elif value == 2:
            duplex = 2

    # Process c2900PortDuplexState
    # The Cisco 3500XL is known to report incorrect duplex values.
    # Obsolete device, doesn't make sense supporting it.
    elif 'c2900PortLinkbeatStatus' in metadata:
        status_link = metadata['c2900PortLinkbeatStatus']
        status_duplex = metadata['c2900PortDuplexStatus']

        if status_link == 3:
            # If no link beats (Not AutoNegotiate)
            if status_duplex == 1:
                duplex = 2
            elif status_duplex == 2:
                duplex = 1
        else:
            # If link beats (AutoNegotiate)
            if status_duplex == 1:
                duplex = 4
            elif status_duplex == 2:
                duplex = 3

    # Return
    return duplex
