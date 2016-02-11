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

## Features
infoset has the following features:

1. Open source.
2. Written in python, a modern language.
3. Easy configuration.
4. Threaded polling of devices for data. Fast.
5. Support for Cisco and Juniper gear. More expected to added with time.
6. Support for SNMPv2 and/or SNMPv3 for all configured network devices.

We are always looking for more contributors!

## Support
The project currently only supports Linux distros that natively support python 3 for ease of portability.

## Inspiration
The project took inspiration from switchmap whose creator, Pete Siemsen, has been providing guidance.

## Oversight
infoset is a student collaboration between:

1. The University of the West Indies Computing Society. (Kingston, Jamaica)
2. The University of Techology, IEEE Student Branch. (Kingston, Jamaica)
3. The Palisadoes Foundation http://www.palisadoes.org

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
# sudo apt-get install python3 python3-pip python3-yaml pep8
# pip3 install pysnmp pylint pep257
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

# Configuration Samples

The `examples/` directory includes a number of sample files. These will now be explained.

## Apache Configuration Samples

The `examples/apache` directory includes sample files to create a:

1. dedicated infoset site (`sites-available.example.org.conf`)
2. URI of an existing site (`conf-available.example.conf`)

## infoset Configuration Samples

The `examples/etc` directory includes a sample files that can be edited. infoset assumes all files in this directory, or any other specified configuration directory, only contains infoset configuration files. Most user will only need to edit the three files supplied.

Feel free to use the `etc/` directory as your permanent configuration file location.

### Sample Configuration File
Here is a sample configuration file that will be explained later in detail. infoset will attempt to contact hosts with each of the parameter sets in the `snmp_group` section till successful.
```
web_directory: /home/example/public_html
data_directory: /home/example/infoset/data

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
#### Configuration File Details Table

|Parameter|Description|
| --- | --- |
| data_directory: | The data directory where all infostor data will be kept. This can be the `data/` directory.|
| web_directory: | The directory where all infostor HTML files will be kept. Make this directory your web root.|
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
```
$ bin/toolbox.py test --directory etc/  --host host1
```

## Polling All Devices
This command will execute against all configured hosts and create appropriate YAML files in the configuration file's `$DATA_DIRECTORY/snmp` directory
```
$ bin/toolbox.py poll --directory etc/
```

## Creating Web Pages for All Devices
For best results, run this command after polling is complete.

This command will execute against all configured hosts and create appropriate HTML files in the configuration file's `$WEB_DIRECTORY` directory
```
$ bin/toolbox.py pagemaker --directory etc/
```

Your webserver will now be able to access the newest HTML in `$WEB_DIRECTORY`.

# Next Steps
There are many dragons to slay and kingdoms to conquer!
## Contribute
Here are a few things to know.

1. Contributions are always welcome. Contact our team for more.
2. View our contributor guidelines here: https://github.com/UWICompSociety/infoset/blob/master/CONTRIBUTING.md
3. View our guidelines for committing code here: https://github.com/UWICompSociety/infoset/blob/master/COMMITTERS.md

## Mailing list
Our current mailing list is: https://groups.google.com/forum/#!forum/gdg-jamaica
## New Features
Visit our GitHub issues for a full list of features and bug fixes. https://github.com/UWICompSociety/infoset/issues
## Design Overview
Visit our wiki's infoset document for the rationale of the design. http://wiki.palisadoes.org/index.php/Infoset
## Sample Output
Visit http://calico.palisadoes.org/infoset to view infoset's latest stable web output.
