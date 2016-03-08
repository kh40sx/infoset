"""Infoset snmp package."""

from base_query import Query

from snmp import jm_iana_enterprise

from infoset.snmp.cisco.mib_ciscoc2900 import CiscoC2900Query
from snmp.cisco.mib_ciscocdp import CiscoCdpQuery
from snmp.cisco.mib_ciscoietfip import CiscoCiscoIetfIpQuery
from snmp.cisco.mib_ciscostack import CiscoStackQuery
from snmp.cisco.mib_ciscovlanmembership import CiscoVlanMembershipQuery
from snmp.cisco.mib_ciscovtp import CiscoVtpQuery

from snmp.juniper.mib_junipervlan import JuniperVlanQuery

from snmp.mib_bridge import BridgeQuery
from snmp.mib_entity import EntityQuery
from snmp.mib_essswitch import EssSwitchQuery
from snmp.mib_etherlike import EtherlikeQuery
from snmp.mib_if import IfQuery
from snmp.mib_ip import IpQuery
from snmp.mib_ipv6 import Ipv6Query
from snmp.mib_lldp import LldpQuery
from snmp.mib_qbridge import QbridgeQuery
from snmp.mib_snmpv2 import Snmpv2Query

__all__ = ('cisco', 'juniper')

queries = [C2900Query, VtpQuery, IetfipQuery, CdpQuery, StackQuery,
           VlanMembershipQuery, Snmpv2Query, IfQuery, BridgeQuery,
           IpQuery, Ipv6Query, EtherlikeQuery, EntityQuery, LldpQuery,
           EssswitchQuery, JuniperVlanQuery, QbridgeQuery]


def getQueries(tag):
    return [query for query in queries if tag in query.tags]
