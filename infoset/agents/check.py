#!/usr/bin/env python3

"""Demonstration Script that extracts agent data from cache directory files.

This could be a modified to be a daemon

"""

# Standard libraries
import os
import time
import subprocess

# Pip3 libraries
import psutil

# Infoset libraries
from infoset.utils import jm_configuration
from infoset.utils import log
from infoset.utils import hidden
from infoset.utils import jm_general


def process():
    """Make sure the correct agents are running.

    Args:
        None

    Returns:
        None

    """
    # Get list of configured agents
    config = jm_configuration.Config()
    agents = config.agents()

    # Process each agent
    for agent_dict in agents:
        # Get agent_name
        agent_name = agent_dict['agent_name']
        agentconfig = jm_configuration.ConfigAgent(agent_name)

        # Check for agent existence
        if agentconfig.agent_enabled() is True:
            _check_when_enabled(agent_name)

        else:
            # Shutdown agent if running
            _check_when_disabled(agent_name)


def _check_when_disabled(agent_name):
    """Stop agent.

    Args:
        agent_filepath: Filepath of agent to be restarted.
        agent_name: Agent name

    Returns:
        None

    """
    # Initialize key variables
    agentconfig = jm_configuration.ConfigAgent(agent_name)
    agent_filename = agentconfig.agent_filename()

    # Get agent status variables
    root_dir = jm_general.root_directory()
    agent_filepath = ('%s/%s') % (root_dir, agent_filename)
    pid = hidden.File()
    pidfile = pid.pid(agent_name)

    # Shutdown agent if running
    if os.path.isfile(pidfile) is True:
        with open(pidfile, 'r') as f_handle:
            pidvalue = int(f_handle.readline().strip())
        if psutil.pid_exists(pidvalue) is True:
            log_message = (
                'Agent "%s" is alive, but should be disabled. '
                'Attempting to stop.'
                '') % (agent_name)
            log.log2quiet(1032, log_message)
            _stop(agent_filepath, agent_name)


def _check_when_enabled(agent_name):
    """Stop agent.

    Args:
        agent_filepath: Filepath of agent to be restarted.
        agent_name: Agent name

    Returns:
        None

    """
    # Initialize key variables
    agentconfig = jm_configuration.ConfigAgent(agent_name)
    agent_filename = agentconfig.agent_filename()

    # Get agent status variables
    root_dir = jm_general.root_directory()
    agent_filepath = ('%s/%s') % (root_dir, agent_filename)
    pid = hidden.File()
    pidfile = pid.pid(agent_name)

    # Ignore agents that cannot be found
    if os.path.isfile(agent_filepath) is False:
        log_message = (
            'Agent executable file %s listed in the '
            'configuration file '
            'of agent "%s" does not exist. Please fix.'
            '') % (agent_filepath, agent_name)
        log.log2quiet(1075, log_message)
        return

    # Check for pid file
    if os.path.isfile(pidfile) is True:
        with open(pidfile, 'r') as f_handle:
            pidvalue = int(f_handle.readline().strip())

        # Check if service died catastrophically. No PID file
        if psutil.pid_exists(pidvalue) is False:
            log_message = (
                'Agent "%s" is dead. Attempting to restart.'
                '') % (agent_name)
            log.log2quiet(1076, log_message)

            # Remove PID file and restart
            os.remove(pidfile)
            _restart(agent_filepath, agent_name)

        else:
            # Check if agent hung without updating the PID
            if agentconfig.monitor_agent_pid() is True:
                try:
                    mtime = os.path.getmtime(pidfile)
                except OSError:
                    mtime = 0
                if mtime < int(time.time()) - (60 * 10):
                    _restart(agent_filepath, agent_name)


def _stop(agent_filepath, agent_name):
    """Stop agent.

    Args:
        agent_filepath: Filepath of agent to be restarted.
        agent_name: Agent name

    Returns:
        None

    """
    # Restart
    log_message = (
        'Stopping agent "%s" as it is disabled, but running.'
        '') % (agent_name)
    log.log2quiet(1033, log_message)
    command2run = ('%s --stop --force') % (agent_filepath)
    _execute(command2run)


def _restart(agent_filepath, agent_name):
    """Restart agent.

    Args:
        agent_filepath: Filepath of agent to be restarted.
        agent_name: Agent name

    Returns:
        None

    """
    # Restart
    log_message = (
        'Starting agent "%s" as it is enabled, but stopped.'
        '') % (agent_name)
    log.log2quiet(1077, log_message)
    command2run = ('%s --start') % (agent_filepath)
    _execute(command2run)


def _execute(command):
    """Run command on CLI.

    Args:
        command: Command to run

    Returns:
        None

    """
    # Run command
    subprocess.run(command.split())
