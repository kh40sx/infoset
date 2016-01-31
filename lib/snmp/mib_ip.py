#!/usr/bin/env python3
"""Class interacts with devices supporting IP-MIB."""


import binascii
from collections import defaultdict


# Import project libraries
from snmp import snmp_manager


class Query(object):

    """Class interacts with devices supporting IP-MIB.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, snmp_params):
        """Function for intializing the class.

        Args:
            snmp_params: SNMP parameters for querying the host

        Returns:
            None

        """
        # Define query object
        self.snmp_query = snmp_manager.Interact(snmp_params)

    def supported(self):
        """Return device's support for the MIB.

        Args:
            None

        Returns:
            validity: True if supported

        """
        # Support OID
        validity = True

        # Return
        return validity

    def layer3(self):
        """Get layer 3 data from device.

        Args:
            None

        Returns:
            final: Final results

        """
        # Initialize key variables
        final = defaultdict(lambda: defaultdict(dict))

        # Get interface ipNetToMediaTable, data
        values = self.ipnettomediatable()
        for key, value in values.items():
            final['ipNetToMediaTable'][key] = value

        # Return
        return final

    def ipnettomediatable(self):
        """Return dict of ipNetToMediaTable, the device's ARP table.

        Args:
            None

        Returns:
            data_dict: Dict of MAC addresses keyed by IPv4 address

        """
        # Initialize key variables
        data_dict = {}

        # Process
        oid = '.1.3.6.1.2.1.4.22.1.2'
        results = self.snmp_query.walk(oid, normalized=False)
        for key, value in sorted(results.items()):
            # Determine IP address
            nodes = key.split('.')
            octets = nodes[-4:]
            ipaddress = '.'.join(octets)

            # Determine MAC address
            macaddress = binascii.hexlify(value).decode('utf-8')

            # Create ARP table entry
            data_dict[ipaddress] = macaddress.lower()

        # Return data
        return data_dict
