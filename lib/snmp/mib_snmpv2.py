#!/usr/bin/env python3
"""Class interacts with devices supporting SNMPv2-MIB."""

from collections import defaultdict

# Import project libraries
from snmp import snmp_manager


class Query(object):

    """Class interacts with devices supporting SNMPv2-MIB.

    Args:
        None

    Returns:
        None

    Key Methods:

        supported: Queries the device to determine whether the MIB is
            supported using a known OID defined in the MIB. Returns True
            if the device returns a response to the OID, False if not.

        system: Returns all relevant system information from the device.
            In some cases a system will have multiple subsystems that are
            covered by an OID. (eg. module / circuit board serial numbers).
            It will therefore be impossible to have a consistent key format
            for data values returned. Data returned by this method will
            therefore be keyed by :
            1) MIB name (primary key)
            2) OID name in the MIB, (secondary key),
            3) Leaf value, or zero (0) if there are no leaves.

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
        oid = '.1.3.6.1.2.1.1.1.0'

        # Return nothing if oid doesn't exist
        if self.snmp_query.oid_exists(oid) is True:
            validity = True

        # Return
        return validity

    def system(self):
        """Get system data from device.

        Args:
            None

        Returns:
            final: Final results

        """
        # Initialize key variables
        data_dict = defaultdict(lambda: defaultdict(dict))
        final = {}
        getvalues = [0]
        key = 0

        # Process
        oidroot = '.1.3.6.1.2.1.1'
        for node in range(1, 7):
            oid = ('%s.%s.0') % (oidroot, node)
            results = self.snmp_query.get(oid, normalized=True)
            for value in results.values():
                getvalues.append(value)

        # Assign values
        data_dict['sysDescr'][key] = getvalues[1].decode('utf-8')
        data_dict['sysObjectID'][key] = getvalues[2].decode('utf-8')
        data_dict['sysUpTime'][key] = int(getvalues[3])
        data_dict['sysContact'][key] = getvalues[4].decode('utf-8')
        data_dict['sysName'][key] = getvalues[5].decode('utf-8')
        data_dict['sysLocation'][key] = getvalues[6].decode('utf-8')

        # Return
        final['SNMPv2-MIB'] = data_dict
        return final
