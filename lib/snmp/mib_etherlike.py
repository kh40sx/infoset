#!/usr/bin/env python3
"""Module for ETHERLIKE-MIB."""

import sys
from collections import defaultdict

# Import project libraries
from snmp import snmp_manager


class Query(object):

    """Class interacts with ETHERLIKE-MIB.

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

        # Get one OID entry in MIB
        oid = '.1.3.6.1.4.1.9.9.46.1.3.1.1.2'

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

        # Get interface dot3StatsDuplexStatus data
        values = self.dot3statsduplexstatus()
        for key, value in values.items():
            final[key]['dot3StatsDuplexStatus'] = value

        # Return
        return final

    def dot3statsduplexstatus(self):
        """Return dict of ETHERLIKE-MIB dot3StatsDuplexStatus for each port.

        Args:
            None

        Returns:
            data_dict: Dict of dot3StatsDuplexStatus using ifIndex as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.2.1.10.7.2.1.19'
        results = self.snmp_query.walk(oid, normalized=True)
        for key, value in sorted(results.items()):
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict
