#!/usr/bin/env python3
"""Calico utility script.

Calico utility script

"""

import os
import sys
import yaml

# Import project libraries
try:
    import jm_cli
    import jm_configuration
    import jm_general
    from snmp import snmp_manager
    from snmp import snmp_info
except:
    print('Error: Please set your $PYTHONPATH variable')
    sys.exit(2)


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
        do_config(cli_args, config)

    # Show interesting information
    if cli_args.mode == 'test':
        do_test(cli_args, config)

    # Process hosts
    if cli_args.mode == 'run':
        do_run(cli_args, config)


def do_config(cli_args, config):
    """Process 'config' CLI option.

    Args:
        connectivity_check: Set if testing for connectivity

    Returns:
        None

    """
    # Show hosts if required
    if cli_args.hosts is True:
        print('hosts:')
        print(yaml.dump(config.hosts(), default_flow_style=False))

    # Show hosts if required
    if cli_args.snmp_auth is True:
        print('snmp_auth:')
        print(yaml.dump(config.snmp_auth(), default_flow_style=False))


def do_test(cli_args, config):
    """Process 'test' CLI option.

    Args:
        connectivity_check: Set if testing for connectivity

    Returns:
        None

    """
    # Show host information
    validate = snmp_manager.Validate(cli_args.host, config.snmp_auth())
    snmp_params = validate.credentials()

    if bool(snmp_params) is True:
        print('\nValid credentials found:\n')
        print(yaml.dump(snmp_params, default_flow_style=False))
        print('\n')

        # Get SNMP data
        status = snmp_info.Query(snmp_params)
        data = status.everything()

        # Pring result as YAML
        yaml_string = jm_general.dict2yaml(data)
        print(yaml_string)


def do_run(cli_args, config):
    """Process 'run' CLI option.

    Args:
        connectivity_check: Set if testing for connectivity

    Returns:
        None

    """
    # Create directory if needed
    perm_dir = config.snmp_directory()
    temp_dir = ('%s/tmp') % (perm_dir)
    if (os.path.isfile(temp_dir) is False) and (
            os.path.isdir(temp_dir) is False):
        os.makedirs(temp_dir, 0o755)

    # Delete all files in temporary directory
    jm_general.delete_files(temp_dir)

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
            yaml_string = jm_general.dict2yaml(data)

            # Dump data
            temp_file = ('%s/%s.yaml') % (temp_dir, host)
            with open(temp_file, 'w') as file_handle:
                file_handle.write(yaml_string)

            # Verbose output
            if cli_args.verbose is True:
                output = ('Completed run: host %s') % (host)
                print(output)

    # Cleanup, move temporary files. Delete temporary directory
    jm_general.move_files(temp_dir, perm_dir)
    os.rmdir(temp_dir)


if __name__ == "__main__":
    main()
