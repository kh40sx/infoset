#!/usr/bin/env python3
"""infoset Linux agent.

Description:

    Uses Python2 to be compatible with most Linux systems

    This script:
        1) Retrieves a variety of system information
        2) Posts the data using HTTP to a server listed
           in the configuration file

"""
# Standard libraries
import os
import sys
import re
import platform
import logging
from collections import defaultdict
import socket

# pip3 libraries
import psutil

# infoset libraries
try:
    from infoset.agents import agent as Agent
except:
    print('You need to set your PYTHONPATH to include the infoset library')
    sys.exit(2)
from infoset.utils import jm_configuration

logging.getLogger('requests').setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG)


class PollingAgent(object):
    """Infoset agent that gathers data.

    Args:
        None

    Returns:
        None

    Functions:
        __init__:
        populate:
        post:
    """

    def __init__(self, config_dir):
        """Method initializing the class.

        Args:
            config_dir: Configuration directory

        Returns:
            None

        """
        # Initialize key variables
        self.agent_name = '_infoset'

        # Get configuration
        self.config = jm_configuration.ConfigAgent(
            config_dir, self.agent_name)

    def name(self):
        """Return agent name.

        Args:
            None

        Returns:
            value: Name of agent

        """
        # Return
        value = self.agent_name
        return value

    def query(self):
        """Query all remote hosts for data.

        Args:
            None

        Returns:
            None

        """
        # Post data to the remote server
        self.upload()

    def upload(self):
        """Post system data to the central server.

        Args:
            None

        Returns:
            None

        """
        # Get hostname
        hostname = '_infoset'

        # Get the UID for the agent
        uid = Agent.get_uid(hostname)

        # Initialize key variables
        agent = Agent.Agent(uid, self.config, hostname)

        # Update agent with system data
        _update_agent_system(agent)

        # Update agent with disk data
        _update_agent_disk(agent)

        # Update agent with network data
        _update_agent_net(agent)

        # Post data
        success = agent.post()

        # Purge cache if success is True
        if success is True:
            agent.purge()


def _update_agent_system(agent):
    """Update agent with system data.

    Args:
        agent: Agent object
        uid: Unique ID for Agent
        config: Configuration object

    Returns:
        None

    """
    #########################################################################
    # Set non chartable values
    #########################################################################

    agent.populate('release', platform.release(), base_type=None)
    agent.populate('system', platform.system(), base_type=None)
    agent.populate('version', platform.version(), base_type=None)
    dist = platform.linux_distribution()
    agent.populate('distribution', ' '.join(dist), base_type=None)
    agent.populate('cpu_count', psutil.cpu_count(), base_type='floating')

    #########################################################################
    # Set chartable values
    #########################################################################
    agent.populate(
        'process_count', len(psutil.pids()), chartable=True)

    agent.populate(
        'cpu_percentage', psutil.cpu_percent(), chartable=True)

    # Load averages
    (la_01, la_05, la_15) = os.getloadavg()
    agent.populate(
        'load_average_01min', la_01, chartable=True)
    agent.populate(
        'load_average_05min', la_05, chartable=True)
    agent.populate(
        'load_average_15min', la_15, chartable=True)

    # Get CPU times
    agent.populate_named_tuple(
        'cpu', psutil.cpu_times(), base_type='counter64')

    # Get CPU stats
    agent.populate_named_tuple(
        'cpu', psutil.cpu_stats(), base_type='counter64')

    # Get memory utilization
    agent.populate_named_tuple('memory', psutil.virtual_memory())


def _update_agent_disk(agent):
    """Update agent with disk data.

    Args:
        agent: Agent object

    Returns:
        None

    """
    # Initialize key variables
    regex = re.compile(r'^ram\d+$')

    # Get swap utilization
    multikey = defaultdict(lambda: defaultdict(dict))
    counterkey = defaultdict(lambda: defaultdict(dict))
    swap_data = psutil.swap_memory()
    system_list = swap_data._asdict()
    # "label" is named tuple describing partitions
    for label in system_list:
        value = system_list[label]
        if label in ['sin', 'sout']:
            counterkey[label][None] = value
        else:
            multikey[label][None] = value
    agent.populate_dict('swap', multikey)
    agent.populate_dict('swap', counterkey, base_type='counter64')

    # Get filesystem partition utilization
    disk_data = psutil.disk_partitions()
    multikey = defaultdict(lambda: defaultdict(dict))
    # "disk" is named tuple describing partitions
    for disk in disk_data:
        # "source" is the partition mount point
        source = disk.mountpoint
        system_data = psutil.disk_usage(source)
        system_dict = system_data._asdict()
        for label, value in system_dict.items():
            multikey[label][source] = value
    agent.populate_dict('disk_usage', multikey)

    # Get disk I/O usage
    io_data = psutil.disk_io_counters(perdisk=True)
    counterkey = defaultdict(lambda: defaultdict(dict))
    # "source" is disk name
    for source in io_data.keys():
        # No RAM pseudo disks. RAM disks OK.
        if bool(regex.match(source)) is True:
            continue
        system_data = io_data[source]
        system_dict = system_data._asdict()
        for label, value in system_dict.items():
            counterkey[label][source] = value
    agent.populate_dict('disk_io', counterkey, base_type='counter64')


def _update_agent_net(agent):
    """Update agent with network data.

    Args:
        agent: Agent object

    Returns:
        None

    """
    # Get network utilization
    nic_data = psutil.net_io_counters(pernic=True)
    counterkey = defaultdict(lambda: defaultdict(dict))
    for source in nic_data.keys():
        # "source" is nic name
        system_data = nic_data[source]
        system_dict = system_data._asdict()
        for label, value in system_dict.items():
            counterkey[label][source] = value
    agent.populate_dict('network', counterkey, base_type='counter64')


def main():
    """Start the infoset agent.

    Args:
        None

    Returns:
        None

    """
    # Get configuration
    cli = Agent.AgentCLI()
    config_dir = cli.config_dir()
    poller = PollingAgent(config_dir)

    # Do control
    cli.control(poller)


if __name__ == "__main__":
    main()
