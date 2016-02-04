#!/usr/bin/env python3
"""Module for LLDP-MIB."""

import binascii
from collections import defaultdict

# Import project libraries
from snmp import snmp_manager


class Query(object):

    """Class interacts with LLDP-MIB.

    Args:
        None

    Returns:
        None

    Key Methods:

        supported: Queries the device to determine whether the MIB is
            supported using a known OID defined in the MIB. Returns True
            if the device returns a response to the OID, False if not.

        layer1: Returns all needed layer 1 MIB information from the device.
            Keyed by OID's MIB name (primary key), ifIndex (secondary key)

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

        # Get one OID entry in MIB (lldpRemSysName)
        oid = '.1.0.8802.1.1.2.1.4.1.1.9'

        # Return nothing if oid doesn't exist
        if self.snmp_query.oid_exists(oid) is True:
            validity = True

        # Return
        return validity

    def layer1(self):
        """Get layer 1 data from device.

        Args:
            None

        Returns:
            final: Final results

        """
        # Initialize key variables
        final = defaultdict(lambda: defaultdict(dict))

        # Get interface lldpRemSysName data
        values = self.lldpremsysname()
        for key, value in values.items():
            final[key]['lldpRemSysName'] = value

        # Get interface lldpRemSysDesc data
        values = self.lldpremsysdesc()
        for key, value in values.items():
            final[key]['lldpRemSysDesc'] = value

        # Get interface lldpRemPortDesc data
        values = self.lldpremportdesc()
        if values is not None:
            for key, value in values.items():
                final[key]['lldpRemPortDesc'] = value

        # Get interface lldpRemSysCapEnabled data
        values = self.lldpremsyscapenabled()
        if values is not None:
            for key, value in values.items():
                final[key]['lldpRemSysCapEnabled'] = value

        # Return
        return final

    def lldpremsysname(self):
        """Return dict of LLDP-MIB lldpRemSysName for each port.

        Args:
            None

        Returns:
            data_dict: Dict of lldpRemSysName using ifIndex as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.0.8802.1.1.2.1.4.1.1.9'

        # Process results
        results = self.snmp_query.swalk(oid, normalized=False)
        for key, value in sorted(results.items()):
            ifindex = _ifindex(key)
            data_dict[ifindex] = str(bytes(value), encoding='utf-8')

        # Return the interface descriptions
        return data_dict

    def lldpremsyscapenabled(self):
        """Return dict of LLDP-MIB lldpRemSysCapEnabled for each port.

        Args:
            None

        Returns:
            data_dict: Dict of lldpRemSysCapEnabled using ifIndex as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)
        length_in_bits = 16
        base = 16

        # Descriptions
        oid = '.1.0.8802.1.1.2.1.4.1.1.12'

        # Process results
        results = self.snmp_query.swalk(oid, normalized=False)
        for key, value in sorted(results.items()):
            ifindex = _ifindex(key)

            # Convert binary data to hex value
            hex_value = binascii.hexlify(value).decode('utf-8')

            # Convert hex value to right justified 16 character binary string
            binary_string = bin(int(
                hex_value, base))[2:].zfill(length_in_bits)
            data_dict[ifindex] = binary_string

        # Return the interface descriptions
        return data_dict

    def lldpremsysdesc(self):
        """Return dict of LLDP-MIB lldpRemSysDesc for each port.

        Args:
            None

        Returns:
            data_dict: Dict of lldpRemSysDesc using ifIndex as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.0.8802.1.1.2.1.4.1.1.10'

        # Process results
        results = self.snmp_query.swalk(oid, normalized=False)
        for key, value in sorted(results.items()):
            ifindex = _ifindex(key)
            data_dict[ifindex] = str(bytes(value), encoding='utf-8')

        # Return the interface descriptions
        return data_dict

    def lldpremportdesc(self):
        """Return dict of LLDP-MIB lldpRemPortDesc for each port.

        Args:
            None

        Returns:
            data_dict: Dict of lldpRemPortDesc using ifIndex as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.0.8802.1.1.2.1.4.1.1.8'

        # Process results
        results = self.snmp_query.swalk(oid, normalized=False)
        for key, value in sorted(results.items()):
            ifindex = _ifindex(key)
            data_dict[ifindex] = str(bytes(value), encoding='utf-8')

        # Return the interface descriptions
        return data_dict


def _ifindex(oid):
    """Return the ifindex from a CDP OID.

    Args:
        oid: OID

    Returns:
        ifindex: value of the ifindex

    """
    # Initialize key variables
    nodes = oid.split('.')
    ifindex = int(nodes[-2])

    # Return
    return ifindex
