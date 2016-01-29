#!/usr/bin/env python3
"""Class interacts with devices supporting IfMIB."""

import sys
import binascii
from collections import defaultdict
from pprint import pprint

# Import project libraries
from snmp import snmp_manager


class Query(object):

    """Class interacts with devices supporting IfMIB.

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
        oid = '.1.3.6.1.2.1.2.2.1.1.1'

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

        # Get interface ifDescr data
        values = self.ifdescr()
        for key, value in values.items():
            final[key]['ifDescr'] = value

        # Get interface ifAlias data
        values = self.ifalias()
        for key, value in values.items():
            final[key]['ifAlias'] = value

        # Get interface ifSpeed data
        values = self.ifspeed()
        for key, value in values.items():
            final[key]['ifSpeed'] = value

        # Get interface ifOperStatus data
        values = self.ifoperstatus()
        for key, value in values.items():
            final[key]['ifOperStatus'] = value

        # Get interface ifAdminStatus data
        values = self.ifadminstatus()
        for key, value in values.items():
            final[key]['ifAdminStatus'] = value

        # Get interface ifType data
        values = self.iftype()
        for key, value in values.items():
            final[key]['ifType'] = value

        # Get interface ifName data
        values = self.ifname()
        for key, value in values.items():
            final[key]['ifName'] = value

        # Get interface ifIndex data
        values = self.ifindex()
        for key, value in values.items():
            final[key]['ifIndex'] = value

        # Get interface ifPhysAddress data
        values = self.ifphysaddress()
        for key, value in values.items():
            final[key]['ifPhysAddress'] = value

        # Get interface ifHighSpeed data
        values = self.ifhighspeed()
        for key, value in values.items():
            final[key]['ifHighSpeed'] = value

        # Get interface ifInOctets data
        values = self.ifinoctets()
        for key, value in values.items():
            final[key]['ifInOctets'] = value

        # Get interface ifOutOctets data
        values = self.ifoutoctets()
        for key, value in values.items():
            final[key]['ifOutOctets'] = value

        # Get interface ifLastChange data
        values = self.iflastchange()
        for key, value in values.items():
            final[key]['ifLastChange'] = value

        # Return
        return final

    def iflastchange(self):
        """Return dict of IFMIB ifLastChange for each ifIndex for device.

        Args:
            None

        Returns:
            data_dict: Dict of ifLastChange using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.2.1.2.2.1.9'
        results = self.snmp_query.walk(oid, normalized=True)
        for key, value in sorted(results.items()):
            # Process OID
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict

    def ifinoctets(self):
        """Return dict of IFMIB ifInOctets for each ifIndex for device.

        Args:
            None

        Returns:
            data_dict: Dict of ifInOctets using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.2.1.2.2.1.10'
        results = self.snmp_query.walk(oid, normalized=True)
        for key, value in sorted(results.items()):
            # Process OID
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict

    def ifoutoctets(self):
        """Return dict of IFMIB ifOutOctets for each ifIndex for device.

        Args:
            None

        Returns:
            data_dict: Dict of ifOutOctets using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.2.1.2.2.1.16'
        results = self.snmp_query.walk(oid, normalized=True)
        for key, value in sorted(results.items()):
            # Process OID
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict

    def ifdescr(self):
        """Return dict of IFMIB ifDesc for each ifIndex for device.

        Args:
            None

        Returns:
            data_dict: Dict of ifDescr using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.2.1.2.2.1.2'
        results = self.snmp_query.walk(oid, normalized=True)
        for key, value in sorted(results.items()):
            # Process OID
            data_dict[int(key)] = str(bytes(value), encoding='utf-8')

        # Return the interface descriptions
        return data_dict

    def iftype(self):
        """Return dict of IFMIB ifType for each ifIndex for device.

        Args:
            None

        Returns:
            data_dict: Dict of ifType using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.2.1.2.2.1.3'
        results = self.snmp_query.walk(oid, normalized=True)
        for key, value in sorted(results.items()):
            # Process OID
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict

    def ifspeed(self):
        """Return dict of IFMIB ifSpeed for each ifIndex for device.

        Args:
            None

        Returns:
            data_dict: Dict of ifSpeed using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.2.1.2.2.1.5'
        results = self.snmp_query.walk(oid, normalized=True)
        for key, value in sorted(results.items()):
            # Process OID
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict

    def ifadminstatus(self):
        """Return dict of IFMIB ifAdminStatus for each ifIndex for device.

        Args:
            None

        Returns:
            data_dict: Dict of ifAdminStatus using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.2.1.2.2.1.7'
        results = self.snmp_query.walk(oid, normalized=True)
        for key, value in sorted(results.items()):
            # Process OID
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict

    def ifoperstatus(self):
        """Return dict of IFMIB ifOperStatus for each ifIndex for device.

        Args:
            None

        Returns:
            data_dict: Dict of ifOperStatus using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.2.1.2.2.1.8'
        results = self.snmp_query.walk(oid, normalized=True)
        for key, value in sorted(results.items()):
            # Process OID
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict

    def ifalias(self):
        """Return dict of IFMIB ifAlias for each ifIndex for device.

        Args:
            None

        Returns:
            data_dict: Dict of ifAlias using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.2.1.31.1.1.1.18'
        results = self.snmp_query.walk(oid, normalized=True)
        for key, value in sorted(results.items()):
            # Process OID
            data_dict[int(key)] = str(bytes(value), encoding='utf-8')

        # Return the interface descriptions
        return data_dict

    def ifname(self):
        """Return dict of IFMIB ifName for each ifIndex for device.

        Args:
            None

        Returns:
            data_dict: Dict of ifName using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.2.1.31.1.1.1.1'
        results = self.snmp_query.walk(oid, normalized=True)
        for key, value in sorted(results.items()):
            # Process OID
            data_dict[int(key)] = str(bytes(value), encoding='utf-8')

        # Return the interface descriptions
        return data_dict

    def ifindex(self):
        """Return dict of IFMIB ifindex for each ifIndex for device.

        Args:
            None

        Returns:
            data_dict: Dict of ifindex using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.2.1.2.2.1.1'
        results = self.snmp_query.walk(oid, normalized=True)
        for key, value in sorted(results.items()):
            # Process OID
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict

    def ifphysaddress(self):
        """Return dict of IFMIB ifPhysAddress for each ifIndex for device.

        Args:
            None

        Returns:
            data_dict: Dict of ifPhysAddress using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.2.1.2.2.1.6'
        results = self.snmp_query.walk(oid, normalized=True)
        for key, value in sorted(results.items()):
            # Process OID
            macaddress = binascii.hexlify(value).decode('utf-8').lower()
            data_dict[int(key)] = macaddress

        # Return the interface descriptions
        return data_dict

    def ifhighspeed(self):
        """Return dict of IFMIB ifHighSpeed for each ifIndex for device.

        Args:
            None

        Returns:
            data_dict: Dict of ifHighSpeed using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.2.1.31.1.1.1.15'
        results = self.snmp_query.walk(oid, normalized=True)
        for key, value in sorted(results.items()):
            # Process OID
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict
