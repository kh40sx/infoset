#!/usr/bin/env python3
"""Class interacts with devices supporting RFC1213-MIB."""


import binascii
from collections import defaultdict


# Import project libraries
from snmp import snmp_manager


class Query(object):

    """Class interacts with devices supporting RFC1213-MIB.

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
        validity = False

        # Get one OID entry in MIB (atPhysAddress)
        oid = '.1.3.6.1.2.1.3.1.1.2'

        # Return nothing if oid doesn't exist
        if self.snmp_query.oid_exists(oid) is True:
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
        # Return
        return self._ipv4arptable()

    def _ipv4arptable(self):
        """Return dict of the device's ARP table.

        Args:
            None

        Returns:
            data_dict: Dict of MAC addresses keyed by IPv4 address

        """
        # Initialize key variables
        data_dict = defaultdict(lambda: defaultdict(dict))

        # Process
        oid = '.1.3.6.1.2.1.3.1.1.2'
        results = self.snmp_query.walk(oid, normalized=False)
        for key, value in sorted(results.items()):
            nodes = key.split('.')
            octets = nodes[-4:]
            ipaddress = '.'.join(octets)
            macaddress = binascii.hexlify(value).decode('utf-8')
            data_dict['ARPTableIPv4'][
                ipaddress] = macaddress.lower()

        # Return data
        return data_dict
