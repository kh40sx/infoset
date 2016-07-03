#!usr/bin/env python3
"""Class for creating device web pages."""

import tempfile
import textwrap
import time
import os
import queue as Queue
import threading

from infoset.utils import jm_general
from infoset.utils import Translator


# Define a key global variable
THREAD_QUEUE = Queue.Queue()


class HTMLTable(object):
    """Class that creates the device's various HTML tables.

    Methods:
        ethernet: Table of device Ethernet ports
        device: Summary HTML table

    """

    def __init__(self, config, host):
        # Process YAML file for host
        translation = Translator(config, host)
        self.ports = translation.ethernet_data()
        self.summary = translation.system_summary()

    def ethernet(self):
        """Create the ports table for the device.

        Args:
            config: Configuration object
            host: Hostname to process

        Returns:
            html: HTML table string

        """
        # Initialize key variables
        html = _port_table(self.ports)

        # Return
        return html

    def device(self):
        """Create summary table for the devie.

        Args:
            config: Configuration object
            host: Hostname to process

        Returns:
            html: HTML table string

        """
        # Initialize key variables
        html = _device_table(self.summary)

        # Return
        return html


class PageMaker(threading.Thread):
    """Threaded page creation using device YAML files.

    Graciously modified from:
    http://www.ibm.com/developerworks/aix/library/au-threadingpython/

    """

    def __init__(self, queue):
        """Initialize the class.

        Args:
            queue: Threading queue object

        Returns:
            None

        """
        # Start processing
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        """Update the database using threads.

        Args:
            None

        Returns:
            None

        """
        # Start processing
        while True:
            # Get the data_dict
            data_dict = self.queue.get()
            host = data_dict['host']
            config = data_dict['config']
            verbose = data_dict['verbose']
            temp_dir = data_dict['temp_dir']

            # Initialize key variables
            write_file = ('%s/%s.html') % (temp_dir, host)

            # Verbose output
            if verbose is True:
                output = ('Processing on: host %s') % (host)
                print(output)

            # Process YAML file for host
            table = HTMLTable(config, host)

            # Create HTML output
            html = ('%s<h1>%s<h1>\n%s\n<br>\n%s\n<br>\n%s') % (
                _html_header(host), host, table.device(),
                table.ethernet(), _html_footer)
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
    device_file_found = False

    # Create directory if needed
    perm_dir = config.web_directory()
    temp_dir = tempfile.mkdtemp()

    # Delete all files in temporary directory
    jm_general.delete_files(temp_dir)

    # Spawn a pool of threads, and pass them queue instance
    for _ in range(threads_in_pool):
        update_thread = PageMaker(THREAD_QUEUE)
        update_thread.daemon = True
        update_thread.start()

    # Get host data and write to file
    for host in config.hosts():
        # Skip if device file not found
        if os.path.isfile(config.snmp_device_file(host)) is False:
            log_message = (
                'No YAML device file for host %s found in %s. '
                'Run toolbox.py with the "poll" option first.'
                '') % (host, config.snmp_directory())
            jm_general.logit(1018, log_message, False)
            continue
        else:
            device_file_found = True

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

    # Do the rest if device_file_found
    if device_file_found is True:
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

    # Clean up
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


def _get_inactive():
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
        if 'ifHighSpeed' in port_data:
            value = port_data['ifHighSpeed']
            if value >= 1000:
                speed = ('%.0fG') % (value / 1000)
            elif value > 0 and value < 1000:
                speed = ('%.0fM') % (value)
            else:
                speed = 'N/A'
        else:
            speed = 'N/A'

    # Return
    return speed


def _get_cdp(port_data):
    """Return port CDP HTML string.

    Args:
        port_data: Data related to the port

    Returns:
        value: required string

    """
    # Initialize key variables
    value = ''

    # Determine whether CDP is enabled and update string
    if 'cdpCacheDeviceId' in port_data:
        value = ('<p>%s<br>%s<br>%s</p>') % (
            port_data['cdpCacheDeviceId'],
            port_data['cdpCachePlatform'],
            port_data['cdpCacheDevicePort'])

    # Return
    return value


def _get_lldp(port_data):
    """Return port LLDP HTML string.

    Args:
        port_data: Data related to the port

    Returns:
        value: required string

    """
    # Initialize key variables
    value = ''

    # Determine whether LLDP is enabled and update string
    if 'lldpRemSysDesc' in port_data:
        value = ('<p>%s<br>%s<br>%s</p>') % (
            port_data['lldpRemSysName'],
            port_data['lldpRemPortDesc'],
            port_data['lldpRemSysDesc'])

    # Return
    return value


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
        0: 'Unknown',
        1: 'Half',
        2: 'Full',
        3: 'Half-Auto',
        4: 'Full-Auto',
    }

    # Assign duplex
    if _port_up(port_data) is False:
        duplex = 'N/A'
    else:
        if 'jm_duplex' in port_data:
            duplex = options[port_data['jm_duplex']]

    # Return
    return duplex


def _get_vlan(port_data):
    """Return VLAN number.

    Args:
        port_data: Data related to the port

    Returns:
        vlans

    """
    # Initialize key variables
    vlans = 'N/A'

    # Assign VLAN
    if 'jm_trunk' in port_data:
        if port_data['jm_trunk'] is False:
            if 'jm_vlan' in port_data:
                if port_data['jm_vlan'] is not None:
                    values = [str(value) for value in port_data['jm_vlan']]
                    vlans = ' '.join(values)
        else:
            if 'jm_nativevlan' in port_data:
                vlans = str(port_data['jm_nativevlan'])

    # Return
    return vlans


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


def _html_header(host):
    """Display HTML header.

    Args:
        host: Hostname

    Returns:
        html: HTML for header

    """
    # Print header
    html = ("""\
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta http-equiv="refresh" CONTENT="3600">
<META NAME="ROBOTS" CONTENT="NOINDEX, NOFOLLOW">
<title>%s Ports List</title>
</head>
<body>
""") % (host)
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
<META NAME="ROBOTS" CONTENT="NOINDEX, NOFOLLOW">
</head>
<body>
%s
</body>
</html>
""") % (links)

    # Return
    return html


def _port_table(data_dict):
    """Return table with port information.

    Args:
        data_dict: Dict of port data

    Returns:
        output: HTML code for table

    """
    # Initialize key variables
    rows = []
    header = [
        'Port', 'VLAN', 'State', 'Days Inactive',
        'Speed', 'Duplex', 'Port Label', 'CDP', 'LLDP']
    output = '<table>\n'
    thstart = '    <th>'

    # Create header
    output = ('%s%s%s') % (
        output, thstart, (('</th>\n%s') % (thstart)).join(header))
    output = ('%s</th>') % (output)

    # Create rows of data
    for _, port_data in sorted(data_dict.items()):
        # Assign values for Ethernet ports only
        port = port_data['ifName']
        label = port_data['ifAlias']
        speed = _get_speed(port_data)
        inactive = _get_inactive()
        vlan = _get_vlan(port_data)
        state = _get_state(port_data)
        duplex = _get_duplex(port_data)
        cdp = _get_cdp(port_data)
        lldp = _get_lldp(port_data)
        rows.append(
            [port, vlan, state, inactive, speed, duplex, label, cdp, lldp])

    # Loop through list
    for row in rows:
        # Print entry row
        output = ('%s\n    <tr>\n        <td>') % (output)
        output = ('%s%s') % (output, '</td><td>'.join(row))
        output = ('%s</td>\n    </tr>') % (output)

    # Finish the table
    output = ('%s\n</table>') % (output)

    # Return
    return output


def _device_table(data_dict):
    """Return table with device information.

    Args:
        data_dict: Dict of device data

    Returns:
        output: HTML code for table

    """
    # Initialize key variables
    rows = []
    labels = ['sysName', 'sysDescr', 'sysObjectID', 'Uptime']
    values = [
        data_dict['sysName'],
        textwrap.fill(data_dict['sysDescr']).replace('\n', '<br>'),
        data_dict['sysObjectID'],
        _uptime(data_dict['sysUpTime'])
        ]
    output = '<table>'

    # Create rows array
    for index, value in enumerate(values):
        rows.append([labels[index], str(value)])

    # Loop through list
    for row in rows:
        # Print entry row
        output = ('%s\n    <tr>\n        <td>') % (output)
        output = ('%s%s') % (output, '</td><td>'.join(row))
        output = ('%s</td>\n    </tr>') % (output)

    # Finish the table
    output = ('%s\n</table>') % (output)

    # Return
    return output


def _uptime(seconds):
    """Return uptime string.

    Args:
        seconds: Seconds of uptime

    Returns:
        result: Uptime string

    """
    # Initialize key variables
    (minutes, remainder_seconds) = divmod(seconds/100, 60)
    (hours, remainder_minutes) = divmod(minutes, 60)
    (days, remainder_hours) = divmod(hours, 24)

    # Return
    result = ('%.f Days, %d:%02d:%02d') % (
        days, remainder_hours, remainder_minutes, remainder_seconds)
    return result

def cdpcachedeviceid(self, var1, oidonly=False):
        """ Return dict of CISCO-CDP-MIB cdpCacheDeviceId for each port.
        Args:
            var1: Example argument.
            oidonly: Return OID's value, not results, if True
            var: Another example
        Returns:
            data_dict: Dict of cdpCacheDeviceId using ifIndex as key
        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # OID to process
        oid = '.1.3.6.1.4.1.9.9.23.1.2.1.1.6'

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        results = self.snmp_object.swalk(oid, normalized=False)
        for key, value in results.items():
            ifindex = _ifindex(key)
            data_dict[ifindex] = str(bytes(value), encoding='utf-8')

        # Return the interface descriptions
        return data_dict
