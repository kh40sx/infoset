#!/usr/bin/env python3
"""Infoset queries."""

import time
from collections import defaultdict
from pprint import pprint

import jm_iana_enterprise
import jm_general
from getdata.snmp import mib_ciscovlanmembership
from getdata.snmp import mib_ciscovtp
from getdata.snmp import mib_ciscoietfip
from getdata.snmp import mib_snmpv2
from getdata.snmp import mib_if
from getdata.snmp import mib_bridge
from getdata.snmp import mib_ip
from getdata.snmp import mib_ipv6
from getdata.snmp import mib_etherlike
from getdata.snmp import mib_ciscocdp
from getdata.snmp import mib_entity
from getdata.snmp import mib_lldp
from getdata.snmp import mib_ciscostack
from getdata.snmp import mib_ciscoc2900
from getdata.snmp import mib_essswitch
from getdata.snmp import mib_junipervlan


class Query(object):
    """Class interacts with IfMIB devices.

    Args:
        None

    Returns:
        None

    Methods:

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

    def everything(self, do_yaml=False):
        """Get all information from device.

        Args:
            do_yaml: Return YAML if True

        Returns:
            data: Aggregated data

        """
        # Initialize key variables
        data = {}

        # Set string keys
        string_keys = do_yaml

        # Append data
        data['misc'] = self.misc()
        data['layer1'] = self.layer1(string_keys=string_keys)
        data['layer2'] = self.layer2(string_keys=string_keys)
        data['layer3'] = self.layer3(string_keys=string_keys)
        data['system'] = self.system(string_keys=string_keys)

        # Return
        if do_yaml is False:
            return data
        else:
            return jm_general.dict2yaml(data)

    def misc(self):
        """Provide miscellaneous information about device and the poll.

        Args:
            do_yaml: Return YAML if True

        Returns:
            data: Aggregated data

        """
        # Initialize data
        data = defaultdict(lambda: defaultdict(dict))
        data['timestamp'] = int(time.time())
        data['host'] = self.snmp_object.hostname()

        # Get vendor information
        sysobjectid = self.snmp_object.sysobjectid()
        vendor = jm_iana_enterprise.Query(sysobjectid=sysobjectid)
        data['IANAEnterpriseNumber'] = vendor.enterprise()

        # Return
        return data

    def system(self, string_keys=False):
        """Get all system information from device.

        Args:
            do_yaml: Return YAML if True

        Returns:
            data: Aggregated data

        """
        # Initialize data
        data = defaultdict(lambda: defaultdict(dict))
        processed = False

        # Get system information from SNMPv2-MIB
        query = mib_snmpv2.Query(self.snmp_object)
        if query.supported():
            processed = True
            data = _add_system(query, data, string_keys=string_keys)

        # Get information from ENTITY-MIB
        query = mib_entity.Query(self.snmp_object)
        if query.supported() is True:
            processed = True
            data = _add_system(query, data, string_keys=string_keys)

        # Return
        if processed is True:
            return data
        else:
            return None

    def layer1(self, string_keys=False):
        """Get all layer1 information from device.

        Args:
            do_yaml: Return YAML if True

        Returns:
            data: Aggregated data

        """
        # Initialize key values
        data = defaultdict(lambda: defaultdict(dict))
        processed = False

        # Get information from IF-MIB
        query = mib_if.Query(self.snmp_object)
        if query.supported() is True:
            processed = True
            data = _add_layer1(query, data, string_keys=string_keys)

        # Get information from  BRIDGE-MIB
        query = mib_bridge.Query(self.snmp_object)
        if query.supported() is True:
            processed = True
            data = _add_layer1(query, data, string_keys=string_keys)

        # Get information from  CISCO-VLAN-MEMBERSHIP-MIB
        query = mib_ciscovlanmembership.Query(self.snmp_object)
        if query.supported() is True:
            processed = True
            data = _add_layer1(query, data, string_keys=string_keys)

        # Get information from CISCO-VTP-MIB
        query = mib_ciscovtp.Query(self.snmp_object)
        if query.supported() is True:
            processed = True
            data = _add_layer1(query, data, string_keys=string_keys)

        # Get information from EtherLike-MIB
        query = mib_etherlike.Query(self.snmp_object)
        if query.supported() is True:
            processed = True
            data = _add_layer1(query, data, string_keys=string_keys)

        # Get information from CISCO-CDP-MIB
        query = mib_ciscocdp.Query(self.snmp_object)
        if query.supported() is True:
            processed = True
            data = _add_layer1(query, data, string_keys=string_keys)

        # Get information from LLDP-MIB
        query = mib_lldp.Query(self.snmp_object)
        if query.supported() is True:
            processed = True
            data = _add_layer1(query, data, string_keys=string_keys)

        # Get information from CISCO-STACK-MIB
        query = mib_ciscostack.Query(self.snmp_object)
        if query.supported() is True:
            processed = True
            data = _add_layer1(query, data, string_keys=string_keys)

        # Get information from CISCO-C2900-MIB
        query = mib_ciscoc2900.Query(self.snmp_object)
        if query.supported() is True:
            processed = True
            data = _add_layer1(query, data, string_keys=string_keys)

        # Get information from MIB-ESSWITCH
        query = mib_essswitch.Query(self.snmp_object)
        if query.supported() is True:
            processed = True
            data = _add_layer1(query, data, string_keys=string_keys)

        # Get information from JUNIPER-MIB
        query = mib_junipervlan.Query(self.snmp_object)
        if query.supported() is True:
            processed = True
            data = _add_layer1(query, data, string_keys=string_keys)

        # Return
        if processed is True:
            return data
        else:
            return None

    def layer2(self, string_keys=False):
        """Get all layer2 information from device.

        Args:
            do_yaml: Return YAML if True

        Returns:
            data: Aggregated data

        """
        # Initialize key variables
        data = defaultdict(lambda: defaultdict(dict))
        processed = False

        # Get VLAN table information (Cisco)
        query = mib_ciscovtp.Query(self.snmp_object)
        if query.supported() is True:
            processed = True
            data = _add_layer2(query, data, string_keys=string_keys)

        # Get VLAN information from JUNIPER-MIB
        query = mib_junipervlan.Query(self.snmp_object)
        if query.supported() is True:
            processed = True
            data = _add_layer2(query, data, string_keys=string_keys)

        # Return
        if processed is True:
            return data
        else:
            return None

    def layer3(self, string_keys=False):
        """Get all layer3 information from device.

        Args:
            do_yaml: Return YAML if True

        Returns:
            data: Aggregated data

        """
        # Initialize key variables
        data = defaultdict(lambda: defaultdict(dict))
        processed = False

        # Get IPv4 information
        query = mib_ip.Query(self.snmp_object)
        if query.supported() is True:
            processed = True
            data = _add_layer3(query, data, string_keys=string_keys)

        # Get IPv6 ARP table information (Cisco)
        query = mib_ciscoietfip.Query(self.snmp_object)
        if query.supported() is True:
            processed = True
            data = _add_layer3(query, data, string_keys=string_keys)

        # Get IPv6 ARP table information (Juniper)
        query = mib_ipv6.Query(self.snmp_object)
        if query.supported() is True:
            processed = True
            data = _add_layer3(query, data, string_keys=string_keys)

        # Return
        if processed is True:
            return data
        else:
            return None


def _add_data(source, target, string_keys=False):
    """Add data from source to target dict. Both dicts must have two keys.

    Args:
        source: Source dict
        target: Target dict

    Returns:
        target: Aggregated data

    """
    # Process data
    for primary in source.keys():
        for secondary, value in source[primary].items():
            if string_keys is False:
                target[primary][secondary] = value
            else:
                target[str(primary)][str(secondary)] = value

        # Return
    return target


def _add_layer1(query, original_data, string_keys=False):
    """Add data from successful layer1 MIB query to original data provided.

    Args:
        query: MIB query object
        original_data: Two keyed dict of data

    Returns:
        new_data: Aggregated data

    """
    # Process query
    result = query.layer1()
    new_data = _add_data(
        result, original_data, string_keys=string_keys)

    # Return
    return new_data


def _add_layer2(query, original_data, string_keys=False):
    """Add data from successful layer2 MIB query to original data provided.

    Args:
        query: MIB query object
        original_data: Two keyed dict of data

    Returns:
        new_data: Aggregated data

    """
    # Process query
    result = query.layer2()
    new_data = _add_data(
        result, original_data, string_keys=string_keys)

    # Return
    return new_data


def _add_layer3(query, original_data, string_keys=False):
    """Add data from successful layer3 MIB query to original data provided.

    Args:
        query: MIB query object
        original_data: Two keyed dict of data

    Returns:
        new_data: Aggregated data

    """
    # Process query
    result = query.layer3()
    new_data = _add_data(
        result, original_data, string_keys=string_keys)

    # Return
    return new_data


def _add_system(query, data, string_keys=False):
    """Add data from successful system MIB query to original data provided.

    Args:
        query: MIB query object
        data: Three keyed dict of data

    Returns:
        data: Aggregated data

    """
    # Process query
    result = query.system()

    # Add tag
    for primary in result.keys():
        for secondary in result[primary].keys():
            for tertiary, value in result[primary][secondary].items():
                if string_keys is False:
                    data[primary][secondary][tertiary] = value
                else:
                    data[str(primary)][str(secondary)][str(tertiary)] = value

    # Return
    return data
