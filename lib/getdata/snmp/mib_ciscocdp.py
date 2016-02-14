#!/usr/bin/env python3
"""Module for CISCO-CDP-MIB."""

from collections import defaultdict


class Query(object):
    """Class interacts with CISCO-CDP-MIB.

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

    def supported(self):
        """Return device's support for the MIB.

        Args:
            None

        Returns:
            validity: True if supported

        """
        # Support OID
        validity = False

        # Get one OID entry in MIB (cdpCacheDeviceId)
        oid = '.1.3.6.1.4.1.9.9.23.1.2.1.1.6'

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
        if values is not None:
            for key, value in values.items():
                final[key]['cdpCacheDevicePort'] = value

        # Return
        return final

    def cdpcachedeviceid(self, oidonly=False):
        """Return dict of CISCO-CDP-MIB cdpCacheDeviceId for each port.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of cdpCacheDeviceId using ifIndex as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # OID to process
        oid = '.1.3.6.1.4.1.9.9.23.1.2.1.1.6'

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        results = self.snmp_object.swalk(oid, normalized=False)
        for key, value in sorted(results.items()):
            ifindex = _ifindex(key)
            data_dict[ifindex] = str(bytes(value), encoding='utf-8')

        # Return the interface descriptions
        return data_dict

    def cdpcacheplatform(self, oidonly=False):
        """Return dict of CISCO-CDP-MIB cdpCachePlatform for each port.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of cdpCachePlatform using ifIndex as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # OID to process
        oid = '.1.3.6.1.4.1.9.9.23.1.2.1.1.8'

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        results = self.snmp_object.swalk(oid, normalized=False)
        for key, value in sorted(results.items()):
            ifindex = _ifindex(key)
            data_dict[ifindex] = str(bytes(value), encoding='utf-8')

        # Return the interface descriptions
        return data_dict

    def cdpcachedeviceport(self, oidonly=False):
        """Return dict of CISCO-CDP-MIB cdpCacheDevicePort for each port.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of cdpCacheDevicePort using ifIndex as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # OID to process
        oid = '.1.3.6.1.4.1.9.9.23.1.2.1.1.7'

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        results = self.snmp_object.swalk(oid, normalized=False)
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
