#!/usr/bin/env python3
"""Module for Q-BRIDGE-MIB."""


from collections import defaultdict

# Import project libraries
from infoset.snmp import mib_bridge


class Query(object):
    """Class interacts with Q-BRIDGE-MIB.

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

    def __init__(self, snmp_object):
        """Function for intializing the class.

        Args:
            snmp_object: SNMP Interact class object from snmp_manager.py

        Returns:
            None

        """
        # Define query object
        self.snmp_object = snmp_object

        # Get a mapping of dot1dbaseport values to the corresponding ifindex
        bridge_mib = mib_bridge.Query(self.snmp_object)
        self.baseportifindex = bridge_mib.dot1dbaseport_2_ifindex()

    def supported(self):
        """Return device's support for the MIB.

        Args:
            None

        Returns:
            validity: True if supported

        """
        # Support OID
        validity = False

        # Get one OID entry in MIB (dot1qPvid)
        oid = '.1.3.6.1.2.1.17.7.1.4.5.1.1'

        # Return nothing if oid doesn't exist
        if self.snmp_object.oid_exists(oid) is True:
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

        # Get interface dot1qPvid data
        values = self.dot1qpvid()
        for key, value in values.items():
            final[key]['dot1qPvid'] = value

        # Return
        return final

    def dot1qpvid(self):
        """Return dict of Q-BRIDGE-MIB dot1qPvid per port.

        Args:
            None

        Returns:
            data_dict: Dict of dot1qPvid using ifIndex as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process OID
        oid = '.1.3.6.1.2.1.17.7.1.4.5.1.1'
        results = self.snmp_object.walk(oid, normalized=True)
        for key, value in results.items():
            ifindex = self.baseportifindex[int(key)]
            data_dict[ifindex] = value

        # Return
        return data_dict
