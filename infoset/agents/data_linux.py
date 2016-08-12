#!/usr/bin/env python3
"""infoset helper for the Linux agent.

Description:

    Uses Python2 to be compatible with most Linux systems


"""
# Standard libraries
import os
import re
import platform
from collections import defaultdict

# pip3 libraries
import psutil


def getall(agent):
    """Get all agent data.

    Data is specific to the linux server on which this instance of
    infoset is installed.

    Args:
        agent: Agent object

    Returns:
        None

    """
    # Update agent with system data
    _update_agent_system(agent)

    # Update agent with disk data
    _update_agent_disk(agent)

    # Update agent with network data
    _update_agent_net(agent)


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
