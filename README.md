# infoset


## About
infoset is Python 3 inventory system that reports and tabulates the status of network connected devices. The information reported includes:

1. Open Systems Interconnection model (OSI model) data such as:
  1. Layer 1 information (Network port names, speed, state, neighbors)
  2. Layer 2 information (VLANs, 802.1q trunk links)
  3. Layer 3 information (ARP information)
2. System status

The project is not:
1. _A monitoring system_: It does not report information that is likely to change in under 4 hours. Projects such as Nagios are more suitable for this purpose.
2. _A graphing system_: and therefore will not collect historical data likely to change in under 4 hours. Projects such as Cacti are more suitable for this purpose.

As the project is an inventory system, there is some scope for parallel projects to chart changes in resources audited by the project.

## Support
The project currently only supports Linux distros that natively support python 3 for ease of portability.

## Inspiration
The project took inspiration from switchmap whose creator, Pete Siemsen, has been providing guidance.

## Oversight
infoset is a student collaboration between:
1. The University of the West Indies Computing Society. (Kingston, Jamaica)
2. The University of Techology, IEEE Student Branch. (Kingston, Jamaica)
3. The Palisadoes Foundation

And many others.

# Intallation and Initial Setup
There are a number of small steps that need to be taken to get infoset to work.
## Download
Download and extract the infoset archive in your favorite directory.
## Linux Package Installation
The project can be setup on your server or workstation by issuing the following commands:
### Ubuntu / Debian
The commands are:
```
sudo apt-get install python3 python3-pip python3-yaml
pip3 install pysnmp pylint pep257 pep8
```
###Fedora
The commands are:
```
# sudo apt-get install python3 python3-pip python3-PyYAML
# pip3 install pysnmp pylint pep257 pep8
```
## Linux $PYTHONPATH Environment Setup

You will need to setup your PYTHONPATH environment variable to include the following directories.
```
$INSTALLATION_DIRECTORY/lib 
```
For example, if your installation directory is ```/opt/infoset```, then you must issue the following commands prior to running the application.
```
$ PYTHONPATH="${PYTHONPATH}:/opt/infoset/lib"
$ export PYTHONPATH
```
# Configuration
The `/etc` directory includes a sample file that can be edited. infoset assumes all files in this directory, or any other specified configuration directory, only contains infoset configuration files. Most user will only need to edit the three files supplied.

## Sample Configuration File
Here is a sample configuration file that will be explained later in detail. infoset will attempt to contact hosts with each of the parameter sets in the `snmp_group` section till successful.
```
hosts:
    - host1
    - host2
    - host3

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
### Configuration File Details Table

|Parameter|Description|
| --- | --- |
|data_directory: | The data directory where all infostor data will be kept. |
| hosts: | YAML key describing hosts. All hosts are listed under this key.|
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

# The Toolbox.py Script
infoset comes with a handy `toolbox.py` script
## Testing Host Connectivity
You can test connectivity to a host using this command where the configuration directory is `etc/` and the host is `host1`
`$ bin/toolbox.py test --directory etc/  --host host1`

## Polling All Devices
This command will execute against all configured hosts and create appropriate HTML files in the configuration file's `$DATA_DIRECTORY/snmp` directory
`$ bin/toolbox.py run --directory etc/`

You may want to set your webserver to inspect the data in your `$DATA_DIRECTORY/snmp` to view the results of this command.

# Next Steps
There are many dragons to slay and kingdoms to conquer!
## Contribute
Contributions are always welcome. Contact our team for more.
## New Features
Visit our wiki for a complete requirements document.
## Sample Output
Visit http://calico.palisadoes.org/infoset to view infoset's latest stable web output.