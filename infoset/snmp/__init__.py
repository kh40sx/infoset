"""Infoset snmp package"""

from infoset.snmp import jm_iana_enterprise
from infoset.snmp.cisco.mib_c2900 import C2900Query
from infoset.snmp.cisco.mib_vtp import VtpQuery
from infoset.snmp.cisco.mib_ietfip import IetfipQuery
from infoset.snmp.cisco.mib_cdp import CdpQuery
from infoset.snmp.cisco.mib_stack import StackQuery
from infoset.snmp.cisco.vlanmembership import VlanMembershipQuery
from infoset.snmp.mib_snmpv2 import Snmpv2Query
from infoset.snmp.mib_if import IfQuery
from infoset.snmp.mib_bridge import BridgeQuery
from infoset.snmp.mib_ip import IpQuery
from infoset.snmp.mib_ipv6 import Ipv6Query
from infoset.snmp.mib_etherlike import EtherlikeQuery
from infoset.snmp.mib_entity import EntityQuery
from infoset.snmp.mib_lldp import LldpQuery
from infoset.snmp.mib_essswitch import EssswitchQuery
from infoset.snmp.juniper.mib_junipervlan import JuniperVlanQuery
from infoset.snmp.mib_qbridge import QbridgeQuery

queries = [C2900Query,VtpQuery,IetfipQuery,CdpQuery,StackQuery,VlanMembershipQuery,
           Snmpv2Query,IfQuery,BridgeQuery,IpQuery,Ipv6Query,EtherlikeQuery,
           EntityQuery,LldpQuery,EssswitchQuery,JuniperVlanQuery,QbridgeQuery]

def getQueries():
    return queries
