#!/usr/bin/env python3
"""Module for CISCO-VLAN-MEMBERSHIP-MIB."""

from collections import defaultdict

# Import project libraries
from getdata.snmp import snmp_manager


class Query(object):

    """Class interacts with CISCO-VLAN-MEMBERSHIP-MIB.

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

        # Get one OID entry in MIB (vmVlan)
        oid = '.1.3.6.1.4.1.9.9.68.1.2.2.1.2'

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

        # Get interface vmVlan data
        values = self.vmvlan()
        for key, value in values.items():
            final[key]['vmVlan'] = value

        # Get interface vmPortStatus data
        values = self.vmportstatus()
        for key, value in values.items():
            final[key]['vmPortStatus'] = value

        # Return
        return final

    def vmvlan(self):
        """Return dict of CISCO-VLAN-MEMBERSHIP-MIB vmVlan for each VLAN.

        Args:
            None

        Returns:
            data_dict: Dict of vmVlan using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.4.1.9.9.68.1.2.2.1.2'

        # Process data
        results = self.snmp_query.swalk(oid, normalized=True)
        for key, value in sorted(results.items()):
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict

    def vmportstatus(self):
        """Return dict of CISCO-VLAN-MEMBERSHIP-MIB vmPortStatus for each VLAN.

        Args:
            None

        Returns:
            data_dict: Dict of vmPortStatus using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.4.1.9.9.68.1.2.2.1.3'

        # Process data
        results = self.snmp_query.swalk(oid, normalized=True)
        for key, value in sorted(results.items()):
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict
