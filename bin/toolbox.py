#!/usr/bin/env python3
"""Calico utility script.

Calico utility script

"""

from pprint import pprint
import yaml
import os

# Import project libraries
import jm_cli
import jm_configuration
from snmp import snmp_manager
from snmp import snmp_info


def main():
    """Main Function.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    additional_help = """\
Utility script for the project.

"""

    # Process the CLI
    cli_object = jm_cli.Process(additional_help=additional_help)
    cli_args = cli_object.args()

    # Process the config
    config = jm_configuration.Read(cli_args.directory)

    # Show configuration data
    if cli_args.mode == 'config':
        # Show hosts if required
        if cli_args.hosts is True:
            print('hosts:')
            print(yaml.dump(config.hosts(), default_flow_style=False))

        # Show hosts if required
        if cli_args.snmp_auth is True:
            print('snmp_auth:')
            print(yaml.dump(config.snmp_auth(), default_flow_style=False))

    # Show interesting information
    if cli_args.mode == 'test':
        # Show host information
        validate = snmp_manager.Validate(cli_args.host, config.snmp_auth())
        snmp_params = validate.credentials()

        if bool(snmp_params) is True:
            print('Valid credentials found:\n')
            print(yaml.dump(snmp_params, default_flow_style=False))
            print('\n\n')

            # Get SNMP data
            status = snmp_info.Query(snmp_params)
            data = status.everything()
            pprint(data, indent=4)

    # Process hosts
    if cli_args.mode == 'run':
        # Get host data and write to file
        for host in config.hosts():
            # Show host information
            validate = snmp_manager.Validate(host, config.snmp_auth())
            snmp_params = validate.credentials()

            # Verbose output
            if cli_args.verbose is True:
                output = ('Processing on: host %s') % (host)
                print(output)

            # Process if valid
            if bool(snmp_params) is True:
                # Get data
                status = snmp_info.Query(snmp_params)
                data = status.everything()

                # Create directory if needed
                directory = ('%s/snmp') % (config.data_directory())
                if (os.path.isfile(directory) is False) and (
                        os.path.isdir(directory) is False):
                    os.makedirs(directory, 0o755)

                # Dump data
                filename = ('%s/%s.json') % (directory, host)
                with open(filename, 'w') as file_handle:
                    pprint(data, stream=file_handle, indent=4)

                # Verbose output
                if cli_args.verbose is True:
                    output = ('Completed run: host %s') % (host)
                    print(output)


if __name__ == "__main__":
    main()
