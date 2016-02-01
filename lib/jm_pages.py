#!/usr/bin/env python3
"""Classes for polling remote hosts for SNMP data."""

import tempfile
import yaml
import time
import os
import queue as Queue
import threading


import jm_general


# Define a key global variable
THREAD_QUEUE = Queue.Queue()


class PageMaker(threading.Thread):

    """Threaded polling.

    Graciously modified from:
    http://www.ibm.com/developerworks/aix/library/au-threadingpython/

    """

    def __init__(self, queue):
        """ Initialize the threads."""
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        """ Update the database using threads."""
        while True:
            # Get the data_dict
            data_dict = self.queue.get()
            host = data_dict['host']
            config = data_dict['config']
            verbose = data_dict['verbose']
            temp_dir = data_dict['temp_dir']

            # Initialize key variables
            write_file = ('%s/%s.html') % (temp_dir, host)
            yaml_file = ('%s/%s.yaml') % (config.snmp_directory(), host)
            data_dict = {}

            # Verbose output
            if verbose is True:
                output = ('Processing on: host %s') % (host)
                print(output)

            # Fail if yaml file doesn't exist
            if os.path.isfile(yaml_file) is False:
                log_message = (
                    'YAML file %s for host %s doesn\'t exist! '
                    'Try polling devices first.') % (yaml_file, host)
                jm_general.logit(1017, log_message, False)

                # Exit thread
                self.queue.task_done()
                return

            # Read file
            with open(yaml_file, 'r') as file_handle:
                yaml_from_file = file_handle.read()
            yaml_data = yaml.load(yaml_from_file)

            # Create dict for layer1 data
            for key, value in yaml_data['layer1'].items():
                data_dict[int(key)] = value

            # Create HTML output
            html = ('%s\n<h1>%s<h1>%s\n%s') % (
                _html_header(), host, _main_table(data_dict), _html_footer)
            with open(write_file, 'w') as file_handle:
                file_handle.write(html)

            # Verbose output
            if verbose is True:
                output = ('Completed run: host %s') % (host)
                print(output)

            # Signals to queue job is done
            self.queue.task_done()


def make(config, verbose=False):
    """Process 'pagemaker' CLI option.

    Args:
        config: Configuration object
        verbose: Verbose output if True

    Returns:
        None

    """
    # Initialize key variables
    threads_in_pool = 10

    # Create directory if needed
    perm_dir = config.web_directory()
    temp_dir = tempfile.mkdtemp()

    # Delete all files in temporary directory
    jm_general.delete_files(temp_dir)

    # Spawn a pool of threads, and pass them queue instance
    for unused_var in range(threads_in_pool):
        update_thread = PageMaker(THREAD_QUEUE)
        update_thread.daemon = True
        update_thread.start()

    # Get host data and write to file
    for host in config.hosts():
        ####################################################################
        #
        # Define variables that will be required for the database update
        # We have to initialize the dict during every loop to prevent
        # data corruption
        #
        ####################################################################
        data_dict = {}
        data_dict['host'] = host
        data_dict['config'] = config
        data_dict['verbose'] = verbose
        data_dict['temp_dir'] = temp_dir
        THREAD_QUEUE.put(data_dict)

    # Wait on the queue until everything has been processed
    THREAD_QUEUE.join()

    # PYTHON BUG. Join can occur while threads are still shutting down.
    # This can create spurious "Exception in thread (most likely raised
    # during interpreter shutdown)" errors.
    # The "time.sleep(1)" adds a delay to make sure things really terminate
    # properly. This seems to be an issue on virtual machines in Dev only
    time.sleep(1)

    # Create index file
    write_file = ('%s/index.html') % (temp_dir)
    index_html = _index_html(config)
    with open(write_file, 'w') as file_handle:
        file_handle.write(index_html)

    # Cleanup, move temporary files to clean permanent directory.
    # Delete temporary directory
    if os.path.isdir(perm_dir):
        jm_general.delete_files(perm_dir)
    else:
        os.makedirs(perm_dir, 0o755)
    jm_general.move_files(temp_dir, perm_dir)
    os.rmdir(temp_dir)


def _port_enabled(port_data):
    """Return whether port is enabled.

    Args:
        port_data: Data related to the port

    Returns:
        active: True if active

    """
    # Initialize key variables
    enabled = False

    # Assign state
    if 'ifAdminStatus' in port_data:
        value = port_data['ifAdminStatus']
        if value == 1:
            enabled = True

    # Return
    return enabled


def _port_up(port_data):
    """Return whether port is up.

    Args:
        port_data: Data related to the port

    Returns:
        active: True if active

    """
    # Initialize key variables
    enabled = False

    # Assign state
    if _port_enabled(port_data) is True:
        if 'ifOperStatus' in port_data:
            if port_data['ifOperStatus'] == 1:
                enabled = True

    # Return
    return enabled


def _get_state(port_data):
    """Return port state string.

    Args:
        port_data: Data related to the port

    Returns:
        state: State string

    """
    # Assign state
    if _port_enabled(port_data) is False:
        state = 'Disabled'
    else:
        if _port_up(port_data) is False:
            state = 'Inactive'
        else:
            state = 'Active'

    # Return
    return state


def _get_inactive(port_data):
    """Return days inactive for port.

    Args:
        port_data: Data related to the port

    Returns:
        inactive: Days the port has been inactive

    """
    # Return
    return 'TBD'


def _get_speed(port_data):
    """Return port speed.

    Args:
        port_data: Data related to the port

    Returns:
        speed: Port speed

    """
    # Assign speed
    if _port_up(port_data) is False:
        speed = 'N/A'
    else:
        value = port_data['ifHighSpeed']
        if value >= 1000:
            speed = ('%.0fG') % (value / 1000)
        else:
            speed = ('%.0fM') % (value)

    # Return
    return speed


def _get_duplex(port_data):
    """Return port duplex string.

    Args:
        port_data: Data related to the port

    Returns:
        duplex: Duplex string

    """
    # Initialize key variables
    duplex = 'Unknown'
    options = {
        1: 'Unknown',
        2: 'Half',
        3: 'Full',
    }

    # Assign duplex
    if _port_up(port_data) is False:
        duplex = 'N/A'
    else:
        if 'dot3StatsDuplexStatus' in port_data:
            value = port_data['dot3StatsDuplexStatus']
            if value in options:
                duplex = options[value]

    # Return
    return duplex


def _get_vlan(port_data):
    """Return VLAN number.

    Args:
        port_data: Data related to the port

    Returns:
        None

    """
    # Assign VLAN
    if 'vmVlan' in port_data:
        vlan = ('%s') % (port_data['vmVlan'])
    else:
        vlan = 'N/A'

    # Return
    return vlan


def _html_footer():
    """Display HTML footer.

    Args:
        None

    Returns:
        html: HTML for footer

    """
    # Print footer
    html = ("""
</body>
</html>
""")
    return html


def _html_header():
    """Display HTML header.

    Args:
        None

    Returns:
        html: HTML for header

    """
    # Print header
    html = ("""\
<html>
<head>
</head>
<body>
""")
    return html


def _index_html(config):
    """Create HTML for index page.

    Args:
        None

    Returns:
        html: HTML for index page

    """
    # Create links
    links = '<h1>Infoset Hosts</h1>'
    for host in config.hosts():
        links = ('%s<br><a href="%s.html">%s</a>') % (links, host, host)

    # Create
    html = ("""\
<html>
<head>
</head>
<body>
%s
</body>
</html>
""") % (links)

    # Return
    return html


def _main_table(data_dict):
    """Return table with report information.

    Args:
        rows: List of rows to make into table rows
        guard_ids: List of guard user_ids

    Returns:
        result: HTML link for ticket

    """
    # Initialize key variables
    rows = []
    header = [
        'Port', 'VLAN', 'State', 'Days Inactive',
        'Speed', 'Duplex', 'Port Label']
    output = '<table>'
    thstart = '<th>'

    # Create header
    output = ('%s%s%s') % (
        output, thstart, (('</th>\n %s') % (thstart)).join(header))
    output = ('%s</th>') % (output)

    # Create rows of data
    for unused_var, port_data in sorted(data_dict.items()):
        # Assign values for Ethernet ports only
        if 'ifType' in port_data:
            if port_data['ifType'] == 6:
                port = port_data['ifName']
                speed = _get_speed(port_data)
                label = port_data['ifAlias']
                inactive = _get_inactive(port_data)
                vlan = _get_vlan(port_data)
                state = _get_state(port_data)
                duplex = _get_duplex(port_data)
                rows.append(
                    [port, vlan, state, inactive, speed, duplex, label])
            else:
                continue
        else:
            continue

    # Loop through list
    for row in rows:
        # Print entry row
        output = ('%s\n <tr>\n <td>') % (output)
        output = ('%s%s') % (output, '</td><td>'.join(row))
        output = ('%s\n  </td>\n </tr>') % (output)

    # Finish the table
    output = ('%s\n</table>\n') % (output)

    # Strip out any duplicated spaces
    output = ' '.join(output.split())

    # Strip out any duplicated line feeds
    output = '\n'.join(output.split())

    # Return
    return output
