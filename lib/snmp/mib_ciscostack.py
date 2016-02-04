#!/usr/bin/env python3
"""Module for CISCO-STACK-MIB."""


from collections import defaultdict

# Import project libraries
from snmp import snmp_manager


class Query(object):
    """Class interacts with CISCO-STACK-MIB.

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

        # Get one OID entry in MIB (portDuplex)
        oid = '.1.3.6.1.4.1.9.5.1.4.1.1.10'

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

        # Get interface portDuplex data
        values = self.portduplex()
        for key, value in values.items():
            final[key]['portDuplex'] = value

        # Return
        return final

    def portduplex(self):
        """Return dict of CISCO-STACK-MIB portDuplex for each port.

        Args:
            None

        Returns:
            data_dict: Dict of portDuplex using ifIndex as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.4.1.9.5.1.4.1.1.10'
        results = self.snmp_query.walk(oid, normalized=True)
        for key, value in sorted(results.items()):
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict
