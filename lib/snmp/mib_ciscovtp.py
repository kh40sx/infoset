#!/usr/bin/env python3
"""Class interacts with CISCO-VTP-MIB."""


from collections import defaultdict

# Import project libraries
from snmp import snmp_manager


class Query(object):

    """Class interacts with CISCO-VTP-MIB.

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

        layer2: Returns all needed layer 2 MIB information from the device.
            Keyed by OID's MIB name (primary key), VLAN number (secondary key)

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

        # Get one OID entry in MIB (vtpVlanState)
        oid = '.1.3.6.1.4.1.9.9.46.1.3.1.1.2'

        # Return nothing if oid doesn't exist
        if self.snmp_query.oid_exists(oid) is True:
            validity = True

        # Return
        return validity

    def layer2(self):
        """Get layer 2 data from device.

        Args:
            None

        Returns:
            final: Final results

        """
        # Initialize key variables
        final = defaultdict(lambda: defaultdict(dict))

        # Get interface vtpVlanName data
        values = self.vtpvlanname()
        for key, value in values.items():
            final[key]['vtpVlanName'] = value

        # Get interface vtpVlanType data
        values = self.vtpvlantype()
        for key, value in values.items():
            final[key]['vtpVlanType'] = value

        # Get interface vtpVlanState data
        values = self.vtpvlanstate()
        for key, value in values.items():
            final[key]['vtpVlanState'] = value

        # Return
        return final

    def layer1(self):
        """Get layer 1 data from device.

        Args:
            None

        Returns:
            final: Final results

        """
        # Initialize key variables
        final = defaultdict(lambda: defaultdict(dict))

        # Get interface vlanTrunkPortDynamicState data
        values = self.vlantrunkportdynamicstate()
        for key, value in values.items():
            final[key]['vlanTrunkPortDynamicState'] = value

        # Get interface vlanTrunkPortDynamicStatus data
        values = self.vlantrunkportdynamicstatus()
        for key, value in values.items():
            final[key]['vlanTrunkPortDynamicStatus'] = value

        # Get interface vlanTrunkPortNativeVlan data
        values = self.vlantrunkportnativevlan()
        for key, value in values.items():
            final[key]['vlanTrunkPortNativeVlan'] = value

        # Get interface vlanTrunkPortEncapsulationType data
        values = self.vlantrunkportencapsulationtype()
        for key, value in values.items():
            final[key]['vlanTrunkPortEncapsulationType'] = value

        # Return
        return final

    def vlantrunkportencapsulationtype(self):
        """Return CISCO-VTP-MIB vlanTrunkPortEncapsulationType per ifIndex.

        Args:
            None

        Returns:
            data_dict: Dict of vlanTrunkPortEncapsulationType
                using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.4.1.9.9.46.1.6.1.1.3'

        # Process results
        results = self.snmp_query.swalk(oid, normalized=True)
        for key, value in sorted(results.items()):
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict

    def vlantrunkportnativevlan(self):
        """Return dict of CISCO-VTP-MIB vlanTrunkPortNativeVlan per ifIndex.

        Args:
            None

        Returns:
            data_dict: Dict of vlanTrunkPortNativeVlan
                using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.4.1.9.9.46.1.6.1.1.5'

        # Process results
        results = self.snmp_query.swalk(oid, normalized=True)
        for key, value in sorted(results.items()):
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict

    def vlantrunkportdynamicstatus(self):
        """Return dict of CISCO-VTP-MIB vlanTrunkPortDynamicStatus per ifIndex.

        Args:
            None

        Returns:
            data_dict: Dict of vlanTrunkPortDynamicStatus
                using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.4.1.9.9.46.1.6.1.1.14'

        # Process results
        results = self.snmp_query.swalk(oid, normalized=True)
        for key, value in sorted(results.items()):
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict

    def vlantrunkportdynamicstate(self):
        """Return dict of CISCO-VTP-MIB vlanTrunkPortDynamicState per ifIndex.

        Args:
            None

        Returns:
            data_dict: Dict of vlanTrunkPortDynamicState
                using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.4.1.9.9.46.1.6.1.1.13'

        # Process results
        results = self.snmp_query.swalk(oid, normalized=True)
        for key, value in sorted(results.items()):
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict

    def vtpvlanname(self):
        """Return dict of CISCO-VTP-MIB vtpVlanName for each VLAN.

        Args:
            None

        Returns:
            data_dict: Dict of vtpVlanName using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.4.1.9.9.46.1.3.1.1.4'

        # Process results
        results = self.snmp_query.swalk(oid, normalized=True)
        for key, value in sorted(results.items()):
            data_dict[int(key)] = str(bytes(value), encoding='utf-8')

        # Return the interface descriptions
        return data_dict

    def vtpvlantype(self):
        """Return dict of CISCO-VTP-MIB vtpVlanType for each VLAN.

        Args:
            None

        Returns:
            data_dict: Dict of vtpVlanType using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.4.1.9.9.46.1.3.1.1.3'

        # Process results
        results = self.snmp_query.swalk(oid, normalized=True)
        for key, value in sorted(results.items()):
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict

    def vtpvlanstate(self):
        """Return dict of CISCO-VTP-MIB vtpVlanState for each VLAN.

        Args:
            None

        Returns:
            data_dict: Dict of vtpVlanState using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.4.1.9.9.46.1.3.1.1.2'

        # Process results
        results = self.snmp_query.swalk(oid, normalized=True)
        for key, value in sorted(results.items()):
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict
