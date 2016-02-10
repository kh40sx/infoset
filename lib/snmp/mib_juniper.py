#!/usr/bin/env python3
"""Module for JUNIPER-MIB."""


from collections import defaultdict

# Import project libraries
from snmp import snmp_manager
from snmp import mib_bridge


class Query(object):
    """Class interacts with JUNIPER-MIB.

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
        self.snmp_params = snmp_params

    def supported(self):
        """Return device's support for the MIB.

        Args:
            None

        Returns:
            validity: True if supported

        """
        # Support OID
        validity = False

        # Get one OID entry in MIB (jnExVlanPortStatus)
        oid = '.1.3.6.1.4.1.2636.3.40.1.5.1.7.1.3'

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

        # Get interface jnExVlanPortStatus data
        values = self.jnexvlanportstatus()
        for key, value in values.items():
            final[key]['jnExVlanPortStatus'] = value

        # Return
        return final

    def jnexvlanportstatus(self):
        """Return dict of JUNIPER-MIB jnExVlanPortStatus per port.

        Args:
            None

        Returns:
            data_dict: Dict of jnExVlanPortStatus using ifIndex as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.4.1.2636.3.40.1.5.1.7.1.3'
        bridge_mib = mib_bridge.Query(self.snmp_params)

        bridge_to_if_index = bridge_mib.dot1dbaseportifindex()

        results = self.snmp_query.walk(oid, normalized=False)
        for key in sorted(results.keys()):
            nodes = key.split('.')
            vlan = nodes[-2]
            bridge_index = nodes[-1]
            new_key = bridge_to_if_index[int(bridge_index)]
            if new_key in data_dict:
                data_dict[new_key].append(vlan)
            else:
                data_dict[new_key] = [vlan]

        # Return the interface descriptions
        return data_dict
