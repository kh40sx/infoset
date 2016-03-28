#!/usr/bin/env python3
"""Class interacts with devices supporting IfMIB."""


from collections import defaultdict
import binascii

from infoset.snmp.base_query import Query


def get_query():
    """Return this module's Query class."""
    return IfQuery


def init_query(snmp_object):
    """Return initialize and return this module's Query class."""
    return IfQuery(snmp_object)


class IfQuery(Query):
    """Class interacts with devices supporting IfMIB.

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

        # Get one OID entry in MIB (ifDescr)
        test_oid = '.1.3.6.1.2.1.2.2.1.1'

        super().__init__(snmp_object, test_oid, tags=['system', 'layer1'])

    def system(self):
        """Get system data from device.

        Args:
            None

        Returns:
            final: Final results

        """
        # Initialize key variables
        final = defaultdict(lambda: defaultdict(dict))

        # Return
        final['IF-MIB']['ifStackStatus'] = self.ifstackstatus()
        return final

    def layer1(self):
        """Get layer 1 data from device using Layer 1 OIDs.

        Args:
            None

        Returns:
            final: Final results

        """
        # Initialize key variables
        final = defaultdict(lambda: defaultdict(dict))

        # Get interface ifDescr data
        _get_data('ifDescr', self.ifdescr, final)

        # Get interface ifAlias data
        _get_data('ifAlian', self.ifalias, final)

        # Get interface ifSpeed data
        _get_data('ifSpeed', self.ifspeed, final)

        # Get interface ifOperStatus data
        _get_data('ifOperStatus', self.ifoperstatus, final)

        # Get interface ifAdminStatus data
        _get_data('ifAdminStatus', self.ifadminstatus, final)

        # Get interface ifType data
        _get_data('ifType', self.iftype, final)

        # Get interface ifName data
        _get_data('ifName', self.ifname, final)

        # Get interface ifIndex data
        _get_data('ifIndex', self.ifindex, final)

        # Get interface ifPhysAddress data
        _get_data('ifPhysAddress', self.ifphysaddress, final)

        # Get interface ifHighSpeed data
        _get_data('ifHighSpeed', self.ifhighspeed, final)

        # Get interface ifInOctets data
        _get_data('ifInOctets', self.ifinoctets, final)

        # Get interface ifOutOctets data
        _get_data('ifOutOctets', self.ifoutoctets, final)

        # Get interface ifLastChange data
        _get_data('ifLastChange', self.iflastchange, final)

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

        # Process OID
        oid = '.1.3.6.1.2.1.2.2.1.9'
        results = self.snmp_object.walk(oid, normalized=True)
        for key, value in results.items():
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

        # Process OID
        oid = '.1.3.6.1.2.1.2.2.1.10'
        results = self.snmp_object.walk(oid, normalized=True)
        for key, value in results.items():
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

        # Process OID
        oid = '.1.3.6.1.2.1.2.2.1.16'
        results = self.snmp_object.walk(oid, normalized=True)
        for key, value in results.items():
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

        # Process OID
        oid = '.1.3.6.1.2.1.2.2.1.2'
        results = self.snmp_object.walk(oid, normalized=True)
        for key, value in results.items():
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

        # Process OID
        oid = '.1.3.6.1.2.1.2.2.1.3'
        results = self.snmp_object.walk(oid, normalized=True)
        for key, value in results.items():
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

        # Process OID
        oid = '.1.3.6.1.2.1.2.2.1.5'
        results = self.snmp_object.walk(oid, normalized=True)
        for key, value in results.items():
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

        # Process OID
        oid = '.1.3.6.1.2.1.2.2.1.7'
        results = self.snmp_object.walk(oid, normalized=True)
        for key, value in results.items():
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

        # Process OID
        oid = '.1.3.6.1.2.1.2.2.1.8'
        results = self.snmp_object.walk(oid, normalized=True)
        for key, value in results.items():
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

        # Process OID
        oid = '.1.3.6.1.2.1.31.1.1.1.18'
        results = self.snmp_object.walk(oid, normalized=True)
        for key, value in results.items():
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

        # Process OID
        oid = '.1.3.6.1.2.1.31.1.1.1.1'
        results = self.snmp_object.walk(oid, normalized=True)
        for key, value in results.items():
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

        # Process OID
        oid = '.1.3.6.1.2.1.2.2.1.1'
        results = self.snmp_object.walk(oid, normalized=True)
        for key, value in results.items():
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

        # Process OID
        oid = '.1.3.6.1.2.1.2.2.1.6'
        results = self.snmp_object.walk(oid, normalized=True)
        for key, value in results.items():
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

        # Process OID
        oid = '.1.3.6.1.2.1.31.1.1.1.15'
        results = self.snmp_object.walk(oid, normalized=True)
        for key, value in results.items():
            # Process OID
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict

    def ifstackstatus(self):
        """Return dict of IFMIB ifStackStatus for each ifIndex for device.

        Args:
            None

        Returns:
            final: Dict of ifStackStatus keyed by the ifIndex of the
                ifstacklowerlayer as primary, and ifstackhigherlayer as
                secondary.

        Summary:
            According to the official IF-MIB file. ifStackStatus is a
            "table containing information on the relationships
            between the multiple sub-layers of network interfaces.  In
            particular, it contains information on which sub-layers run
            'on top of' which other sub-layers, where each sub-layer
            corresponds to a conceptual row in the ifTable.  For
            example, when the sub-layer with ifIndex value x runs over
            the sub-layer with ifIndex value y, then this table
            contains:

              ifStackStatus.x.y=active

            For each ifIndex value, I, which identifies an active
            interface, there are always at least two instantiated rows
            in this table associated with I.  For one of these rows, I
            is the value of ifStackHigherLayer; for the other, I is the
            value of ifStackLowerLayer.  (If I is not involved in
            multiplexing, then these are the only two rows associated
            with I.)

            For example, two rows exist even for an interface which has
            no others stacked on top or below it:

              ifStackStatus.0.x=active
              ifStackStatus.x.0=active"

            In the case of Juniper equipment, VLAN information is only
            visible on subinterfaces of the main interface. For example
            interface ge-0/0/0 won't have VLAN information assigned to it
            directly.

            When a VLAN is assigned to this interface, a subinterface
            ge-0/0/0.0 is automatically created with a non-Ethernet ifType.
            VLAN related OIDs are only maintained for this new subinterface
            only. This makes determining an interface's VLAN based on
            Ethernet ifType more difficult. ifStackStatus maps the ifIndex of
            the primary interface (ge-0/0/0) to the ifIndex of the secondary
            interface (ge-0/0/0.0) which manages higher level protocols and
            data structures such as VLANs and LLDP.

            The primary interface is referred to as the
            ifStackLowerLayer and the secondary subinterface is referred to
            as the ifStackHigherLayer.

        """
        # Initialize key variables
        final = defaultdict(lambda: defaultdict(dict))

        # Process OID
        oid = '.1.3.6.1.2.1.31.1.2.1.3'
        results = self.snmp_object.walk(oid, normalized=False)
        for key in results.keys():
            # Get higher and lower layer index values
            nodes = key.split('.')
            ifstackhigherlayer = int(nodes[-2])
            ifstacklowerlayer = int(nodes[-1])

            # Skip some values
            if ifstacklowerlayer == 0:
                continue

            # Make primary key the lower layer interface ifIndex and the
            # value a list of higher level interface ifIndexes.
            if ifstacklowerlayer in final:
                final[ifstacklowerlayer].append(ifstackhigherlayer)
            else:
                final[ifstacklowerlayer] = [ifstackhigherlayer]

        # Return the interface descriptions
        return final


def _get_data(title, func, dest):
    """Populate dest with data from the given function.

    Args:
        title: The name of the data
        func: The function which will return the data
        dest: a dict which will store the data

    Returns:
        dest: The modified destination dict

    """
    # Get interface ifDescr data
    values = func()
    for key, value in values.items():
        dest[key][title] = value

    return dest
