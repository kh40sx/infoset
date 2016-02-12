#!/usr/bin/env python3
"""Vendor queries."""

# Import project libraries
from getdata.snmp import snmp_manager


class Query(object):
    """Class interacts with devices to get vendor information.

    Args:
        None

    Returns:
        None

    Methods:
        All methods rely on this document to determine vendors
        https://www.iana.org/assignments/
            enterprise-numbers/enterprise-numbers

    """

    def __init__(self, snmp_params):
        """Function for intializing the class.

        Args:
            snmp_params: Dict of SNMP parameters to use in querying device

        Returns:
            None

        """
        # Define query object
        snmp_query = snmp_manager.Interact(snmp_params)

        # Get the sysObjectID.0 value of the device
        sysobjectid = snmp_query.sysobjectid()

        # Get the vendor ID
        nodes = sysobjectid.split('.')
        self.enterprise = int(nodes[7])

    def enterprise_number(self):
        """Return SNMP enterprise number for the device.

        Args:
            None

        Returns:
            self.enterprise: SNMP enterprise number

        """
        return self.enterprise

    def is_cisco(self):
        """Verify whether device is a Cisco device.

        Args:
            None

        Returns:
            value: True if matches vendor

        """
        # Initialize key variables
        value = False

        # Checks system object ID
        if self.enterprise == 9:
            value = True

        # Return
        return value

    def is_juniper(self):
        """Verify whether device is a Juniper device.

        Args:
            None

        Returns:
            value: True if matches vendor

        """
        # Initialize key variables
        value = False

        # Checks system object ID
        if self.enterprise == 2636:
            value = True

        # Return
        return value
