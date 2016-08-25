# infoset Configuration Details

This page has detailed information on how to configure `infoset`. It includes examples for:

1. The main `_infosetd` server agent
2. Linux agents
3. SNMP agents

[TOC]

## infoset Configuration Samples

The `examples/configuration` directory includes a sample files that can be edited. `infoset` assumes all files in this directory, or any other specified configuration directory, only contains `infoset` configuration files. Most user will only need to edit the three files supplied.

You must place your configuration file in the `etc/` directory as your permanent configuration file location.
## Server Configuration

```
server:
    web_directory: /home/infoset/public_html
    data_directory: /opt/infoset/cache/topology
    ingest_cache_directory: /opt/infoset/cache/ingest
    ingest_threads: 20
    agent_threads: 10
    db_hostname: localhost
    db_username: infoset
    db_password: wt8LVA7J5CNWPf75
    db_name: infoset
    hosts:
        - 192.168.1.1
        - 192.168.1.2
```
|Parameter|Description|
| --- | --- |
| server: | YAML key describing the server configuration.|
| data_directory: | Directory where topology data is stored|
| ingest_cache_directory: | Location where the agent data ingester will store its data in the event it cannot communicate with either the database or the server's API|
| ingest_threads: | The maximum number of threads used to ingest data into the database|
| agent_threads: | The maximum number of threads agents on the server polling remote systems will create|
| db_hostname: | The hostname or IP address of the database server.|
| db_username: | The database username|
| db_password: | The database password|
| db_name: | The name of the database|
| hosts: | A list of hosts the server will poll to get network topology information|

## Shared Configuration
There is some information that both the server and agents need to share. This is covered in the `common` section of the configuration.
```
common:
    log_file: /opt/infoset/logs/infoset.log
    language: en
    server: True
```
|Parameter|Description|
| --- | --- |
| common: | YAML key describing the shared server / agent configuration.|
| log_file: | The name of the log file `infoset` uses|
| language: | The language used by the users of infoset.|
| server: | True if this host is running as an `infoset` server|

## Agent Configuration
An `infoset` agent reports data to the central server for charting.

### Shared Agent Configuration
`infoset` agents all need to comunicate with the central server. This example shows how they should be configured to do this.
```
agents_common:
    server_name: 192.168.3.100
    server_port: 5000
    server_https: False
    agent_cache_directory: /opt/infoset/cache/agents
```
|Parameter|Description|
| --- | --- |
| agents_common: | YAML key describing the shared agent configuration.|
| server_name: | The IP address or fully qualified domain name (FQDN) of the central infoset server.|
| server_port: | TCP port on which the server is listening. (Default 5000)|
| server_https: | True if the server is listening on HTTPS. (Set to False as this feature isn't yet enabled)|
| agent_cache_directory: | The directory in which the agent will store its data if it fails to communicate with the central server. This data will be sent immediately upon the server coming back online.|

### Configuring the SNMP Agent

The `infoset` SNMP agent automatically detects the type of device it is polling and will generate the appropriate charts for it. The agent supports the following devices using SNMP:

1. Network devices that support the SNMP IF-MIB. (Most do)
2. Emerson Liebert NMX UPS systems
3. Emerson Liebert FPC power distribution units
4. Servertech power distribution units

This section outlines how it sould be configured.

### SNMP Agent Configuration
The `infoset` SNMP agent configuration is simple:
```
agents:
	...
    ...
    ...
    - agent_name: snmp
      agent_enabled: False
      agent_filename: bin/agents/snmp.py
      agent_hostnames:
        - 192.168.3.100
```
|Parameter|Description|
| --- | --- |
| agents: | YAML key describing configured agents. All agents are listed under this key.|
| agent_name: | Name of the agent (Don't change)|
| agent_enabled: | True if enabled|
| agent_filename: | Name of the agent's filename (Don't change)|
| agent_hostnames: | A list of hostnames to be polled. Each host must be on a separate line and be preceded with a dash "-"|

#### SNMP Groups Configuration
The `infoset` SNMP agent will attempt to query its configured devices using the authentication parameters in the `snmp_groups:` section. `infoset` will attempt to connect using all the configured groups and will remember the group it used on the previous contact.
```
snmp_groups:
    - group_name: Corporate Campus
      snmp_version: 3
      snmp_secname: woohoo
      snmp_community:
      snmp_port: 161
      snmp_authprotocol: sha
      snmp_authpassword: testing123
      snmp_privprotocol: des
      snmp_privpassword: secret_password

    - group_name: Remote Sites
      snmp_version: 3
      snmp_secname: foobar
      snmp_community:
      snmp_port: 161
      snmp_authprotocol: sha
      snmp_authpassword: testing123
      snmp_privprotocol: aes
      snmp_privpassword: secret_password
```
|Parameter|Description|
| --- | --- |
| snmp_groups: | YAML key describing groups of SNMP authentication parameter. All parameter groups are listed under this key.|
| group_name: | Descriptive name for the group|
| snmp_version: | SNMP version. Must be present even if blank. Only SNMP versions 2 and 3 are supported by the project.
| snmp_secname: | SNMP security name (SNMP version 3 only). Must be present even if blank.|
| snmp_community: | SNMP community (SNMP version 2 only). Must be present even if blank.|
| snmp_port: | SNMP Authprotocol (SNMP version 3 only). Must be present even if blank.|
| snmp_authprotocol:| SNMP AuthPassword (SNMP version 3 only). Must be present even if blank. |
| snmp_authpassword:| SNMP PrivProtocol (SNMP version 3 only). Must be present even if blank.|
| snmp_privprotocol:| SNMP PrivProtocol (SNMP version 3 only). Must be present even if blank.|
| snmp_privpassword: | SNMP PrivPassword (SNMP version 3 only). Must be present even if blank.|
| snmp_port:| SNMP UDP port|
