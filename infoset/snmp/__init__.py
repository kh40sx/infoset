"""Infoset snmp package"""

from snmp import jm_iana_enterprise
from snmp.cisco.mib_c2900 import C2900Query
from snmp.cisco.mib_vtp import VtpQuery
from snmp.cisco.mib_ietfip import IetfipQuery
from snmp.cisco.mib_cdp import CdpQuery
from snmp.cisco.mib_stack import StackQuery
from snmp.cisco.vlanmembership import VlanMembershipQuery
from snmp.mib_snmpv2 import Snmpv2Query
from snmp.mib_if import IfQuery
from snmp.mib_bridge import BridgeQuery
from snmp.mib_ip import IpQuery
from snmp.mib_ipv6 import Ipv6Query
from snmp.mib_etherlike import EtherlikeQuery
from snmp.mib_entity import EntityQuery
from snmp.mib_lldp import LldpQuery
from snmp.mib_essswitch import EssswitchQuery
from snmp.juniper.mib_junipervlan import JuniperVlanQuery
from snmp.mib_qbridge import QbridgeQuery

__all__ = ['cisco','juniper']

queries = [C2900Query,VtpQuery,IetfipQuery,CdpQuery,StackQuery,VlanMembershipQuery,
           Snmpv2Query,IfQuery,BridgeQuery,IpQuery,Ipv6Query,EtherlikeQuery,
           EntityQuery,LldpQuery,EssswitchQuery,JuniperVlanQuery,QbridgeQuery]

def getQueries():
    return queries
