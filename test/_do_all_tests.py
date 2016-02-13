#!/usr/bin/env python3
"""Test all the modules."""

import os
import sys
import locale
import subprocess
import argparse
import textwrap


def main():
    """Test all the modules with unittests.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    additional_help = """\
Runs all python unittest programs in a directory \
whose names begin with the string "test_".

"""

    # Process the CLI
    args = get_cli(additional_help=additional_help)

    # Define where the test files are
    test_dir = args.directory

    # Make sure test directory exists
    if os.path.exists(test_dir) is False:
        message = ('Directory %s does not exist.') % (
            test_dir)
        print(message)

    # Get list of test files
    test_files = os.listdir(test_dir)
    for filename in sorted(test_files):
        full_path = ('%s/%s') % (test_dir, filename)

        # Run the test
        if filename.startswith('test_'):
            run_script(full_path)

    # Print
    message = ('\nHooray - All Done OK!\n')
    print(message)


def run_script(cli_string):
    """Run the cli_string UNIX CLI command and record output.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    encoding = locale.getdefaultlocale()[1]
    test_returncode = ('----- Test Return Code '
                       '----------------------------------------')
    test_stdoutdata = ('----- Test Output '
                       '----------------------------------------')
    test_stderrdata = ('----- Test Error '
                       '-----------------------------------------')

    # Say what we are doing
    string2print = ('\nRunning Command: %s') % (cli_string)
    print(string2print)

    # Run update_devices script
    do_command_list = list(cli_string.split(' '))

    # Create the subprocess object
    process = subprocess.Popen(
        do_command_list,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    stdoutdata, stderrdata = process.communicate()
    returncode = process.returncode

    # Crash if the return code is not 0
    if returncode != 0:
        # Print the Return Code header
        string2print = ('\n%s') % (test_returncode)
        print(string2print)

        # Print the Return Code
        string2print = ('\n%s') % (returncode)
        print(string2print)

        # Print the STDOUT header
        string2print = ('\n%s\n') % (test_stdoutdata)
        print(string2print)

        # Print the STDOUT
        for line in stdoutdata.decode(encoding).split('\n'):
            string2print = ('%s') % (line)
            print(string2print)

        # Print the STDERR header
        string2print = ('\n%s\n') % (test_stderrdata)
        print(string2print)

        # Print the STDERR
        for line in stderrdata.decode(encoding).split('\n'):
            string2print = ('%s') % (line)
            print(string2print)

        # All done
        sys.exit(0)


def get_cli(additional_help=None):
    """Return all the CLI options.

    Args:
        None

    Returns:
        args: Namespace() containing all of our CLI arguments as objects
            - filename: Path to the configuration file

    """
    # Initialize key variables
    width = 80

    # Header for the help menu of the application
    parser = argparse.ArgumentParser(
        description=additional_help,
        formatter_class=argparse.RawTextHelpFormatter)

    # CLI argument for the config directory
    parser.add_argument(
        '--directory',
        required=True,
        default=None,
        type=str,
        help=textwrap.fill(
            'Test directory to use.', width=width)
    )
    # Return the CLI arguments
    args = parser.parse_args()

    # Return our parsed CLI arguments
    return args


if __name__ == '__main__':

    # Do the unit test
    main()
