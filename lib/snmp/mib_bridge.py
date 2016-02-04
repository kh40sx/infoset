#!/usr/bin/env python3
"""Class interacts with devices supporting BRIDGE-MIB."""


import binascii
from collections import defaultdict


# Import project libraries
from snmp import snmp_manager


class Query(object):

    """Class interacts with devices supporting BRIDGE-MIB.

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

        # Get one OID entry in MIB (dot1dTpFdbPort)
        oid = '.1.3.6.1.2.1.17.4.3.1.2'

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
        # Return
        return self._macaddresstable()

    def _macaddresstable(self):
        """Return dict of the devices MAC address table.

        Args:
            None

        Returns:
            final: Dict of MAC addresses keyed by ifIndex

        """
        # Initialize key variables
        data_dict = defaultdict(lambda: defaultdict(dict))
        final = defaultdict(lambda: defaultdict(dict))
        ports = self._dot1dtpfdbport()
        macs = self._dot1dtpfdbaddress()

        # Create a dict keyed by ifindex
        for key, value in macs.items():
            if ports[key] not in data_dict:
                data_dict[int(ports[key])] = [value]
            else:
                data_dict[int(ports[key])].append(value)

        # Convert MAC value to bytes in hex format, then convert to string
        for key, value in data_dict.items():
            final[key]['macs'] = []
            for next_mac in value:
                final[key]['macs'].append(next_mac)

        # Return
        return final

    def _dot1dtpfdbport(self):
        """Return dict of BRIDGE-MIB dot1dTpFdbPort data.

        Args:
            None

        Returns:
            data_dict: Dict of dot1dTpFdbPort using the OID nodes
                excluding the OID root as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process values
        oid = '.1.3.6.1.2.1.17.4.3.1.2'
        results = self.snmp_query.walk(oid, normalized=False)
        for key, value in sorted(results.items()):
            new_key = key[len(oid):]
            data_dict[new_key] = value

        # Return data
        return data_dict

    def _dot1dtpfdbaddress(self):
        """Return dict of BRIDGE-MIB dot1dTpFdbAddress data.

        Args:
            None

        Returns:
            data_dict: Dict of dot1dTpFdbAddress using the OID nodes
                excluding the OID root as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process values
        oid = '.1.3.6.1.2.1.17.4.3.1.1'
        results = self.snmp_query.walk(oid, normalized=False)
        for key, value in sorted(results.items()):
            new_key = key[len(oid):]
            macaddress = binascii.hexlify(value).decode('utf-8')
            data_dict[new_key] = macaddress.lower()

        # Return data
        return data_dict
