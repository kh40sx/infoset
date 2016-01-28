#!/usr/bin/env python3
"""Module for CISCO-CDP-MIB."""

from collections import defaultdict

# Import project libraries
from snmp import snmp_manager


class Query(object):

    """Class interacts with CISCO-CDP-MIB.

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

        # Get interface cdpCacheDeviceId data
        values = self.cdpcachedeviceid()
        for key, value in values.items():
            final[key]['cdpCacheDeviceId'] = value

        # Get interface cdpCachePlatform data
        values = self.cdpcacheplatform()
        for key, value in values.items():
            final[key]['cdpCachePlatform'] = value

        # Get interface cdpCacheDevicePort data
        values = self.cdpcachedeviceport()
        for key, value in values.items():
            final[key]['cdpCacheDevicePort'] = value

        # Return
        return final

    def cdpcachedeviceid(self):
        """Return dict of CISCO-CDP-MIB cdpCacheDeviceId for each port.

        Args:
            None

        Returns:
            data_dict: Dict of cdpCacheDeviceId using ifIndex as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.4.1.9.9.23.1.2.1.1.6'
        results = self.snmp_query.walk(oid, normalized=False)
        for key, value in sorted(results.items()):
            ifindex = _ifindex(key)
            data_dict[ifindex] = str(bytes(value), encoding='utf-8')

        # Return the interface descriptions
        return data_dict

    def cdpcacheplatform(self):
        """Return dict of CISCO-CDP-MIB cdpCachePlatform for each port.

        Args:
            None

        Returns:
            data_dict: Dict of cdpCachePlatform using ifIndex as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.4.1.9.9.23.1.2.1.1.8'
        results = self.snmp_query.walk(oid, normalized=False)
        for key, value in sorted(results.items()):
            ifindex = _ifindex(key)
            data_dict[ifindex] = str(bytes(value), encoding='utf-8')

        # Return the interface descriptions
        return data_dict

    def cdpcachedeviceport(self):
        """Return dict of CISCO-CDP-MIB cdpCacheDevicePort for each port.

        Args:
            None

        Returns:
            data_dict: Dict of cdpCacheDevicePort using ifIndex as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.4.1.9.9.23.1.2.1.1.7'
        results = self.snmp_query.walk(oid, normalized=False)
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
