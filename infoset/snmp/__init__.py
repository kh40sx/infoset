"""Infoset snmp package."""

from infoset.snmp.base_query import Query

from infoset.snmp import jm_iana_enterprise

from infoset.snmp.mib_bridge import BridgeQuery
from infoset.snmp.mib_entity import EntityQuery
from infoset.snmp.mib_essswitch import EssSwitchQuery
from infoset.snmp.mib_etherlike import EtherlikeQuery
from infoset.snmp.mib_if import IfQuery
from infoset.snmp.mib_ip import IpQuery
from infoset.snmp.mib_ipv6 import Ipv6Query
from infoset.snmp.mib_lldp import LldpQuery
from infoset.snmp.mib_qbridge import QbridgeQuery
from infoset.snmp.mib_snmpv2 import Snmpv2Query

from infoset.snmp.cisco import CiscoC2900Query
from infoset.snmp.cisco import CiscoCdpQuery
from infoset.snmp.cisco import CiscoIetfIpQuery
from infoset.snmp.cisco import CiscoStackQuery
from infoset.snmp.cisco import CiscoVlanMembershipQuery
from infoset.snmp.cisco import CiscoVtpQuery

from infoset.snmp.juniper import JuniperVlanQuery


__all__ = ('cisco', 'juniper')

QUERIES = [CiscoC2900Query, CiscoVtpQuery, CiscoIetfIpQuery,
           CiscoCdpQuery, CiscoStackQuery, CiscoVlanMembershipQuery,
           Snmpv2Query, IfQuery, BridgeQuery, IpQuery,
           Ipv6Query, EtherlikeQuery, EntityQuery, LldpQuery,
           EssSwitchQuery, JuniperVlanQuery, QbridgeQuery]


def get_queries(layer):
    """Get mib queries which gather information related to a specific OSI layer.

    Args:
        tag: The layer of queries needed

    Returns:
        queries: List of queries tagged the given layer

    """
    return [item for item in QUERIES if layer in item.tags]
