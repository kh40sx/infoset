#!/usr/bin/env python3
"""Vendor queries."""

# Import project libraries
from snmp import snmp_manager


class Query(object):
    """Class interacts with devices to get vendor information.

    Args:
        None

    Returns:
        None

    Methods:

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
        self.sysobjectid = snmp_query.sysobjectid()

    def is_cisco(self):
        """Verify whether device is a Cisco device.

        Args:
            None

        Returns:
            value: True if matches vendor

        """
        # Initialize key variables
        # (The trailing "." in vendor_string is important)
        vendor_string = '.1.3.6.1.4.1.9.'
        value = False

        # Checks system object ID
        if self.sysobjectid.startswith(vendor_string) is True:
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
        # (The trailing "." in vendor_string is important)
        vendor_string = '.1.3.6.1.4.1.2636.'
        value = False

        #Checks system object ID
        if self.sysobjectid.startswith(vendor_string) is True:
            value = True
        return value
