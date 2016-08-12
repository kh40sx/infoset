#!/usr/bin/env python3

"""Demonstration Script that extracts agent data from cache directory files.

This could be a modified to be a daemon

"""

# Standard libraries
import os
import subprocess

# Pip3 libraries
import psutil

# Infoset libraries
from infoset.utils import jm_configuration
from infoset.utils import log
from infoset.utils import hidden
from infoset.utils import jm_general
from infoset import infoset


def process():
    """Make sure the correct agents are running.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    agents = []
    infoset_dir = infoset.__path__[0]
    components = infoset_dir.split(os.sep)
    root_dir = os.sep.join(components[0:-2])

    # Get configuration
    config_directory = os.environ['INFOSET_CONFIGDIR']

    # Get list of configured agents
    agent_directory = ('%s/agents') % (config_directory)
    sub_directories = [result[0] for result in os.walk(agent_directory)]
    for sub_directory in sub_directories:
        if sub_directory == agent_directory:
            continue

        # Get agent names. Ignore '_agentsd' as we don't want to shut
        # ourselves down.
        if sub_directory != '_agentsd':
            agents.append(os.path.basename(sub_directory))

    for agent in agents:
        # Get agent status variables
        config = jm_configuration.ConfigAgent(config_directory, agent)
        filename = ('%s/%s') % (root_dir, config.agent_filename())
        pid = hidden.File()
        pidfile = pid.pid(agent)

        # Ignore agents that cannot be found
        if os.path.isfile(filename) is False:
            log_message = (
                'Agent executable file %s listed in the '
                'configuration file '
                'of agent "%s" does not exist. Please fix.'
                '') % (config.agent_filename(), agent)
            log.log2quiet(1075, log_message)
            continue

        # Check for agent existence
        if config.agent_enabled() is True:
            # Check for pid file
            if os.path.isfile(pidfile) is True:
                with open(pidfile, 'r') as f_handle:
                    pidvalue = int(f_handle.readline().strip())
                if psutil.pid_exists(pidvalue) is False:
                    log_message = (
                        'Agent "%s" is dead. Attempting to restart.'
                        '') % (agent)
                    log.log2quiet(1076, log_message)

                    # Remove PID file and restart
                    os.remove(pidfile)
                    _restart(filename, agent)
            else:
                _restart(filename, agent)
        else:
            # Shutdown agent if running
            if os.path.isfile(pidfile) is True:
                with open(pidfile, 'r') as f_handle:
                    pidvalue = int(f_handle.readline().strip())
                if psutil.pid_exists(pidvalue) is True:
                    log_message = (
                        'Agent "%s" is alive, but should be disabled. '
                        'Attempting to stop.'
                        '') % (agent)
                    log.log2quiet(1032, log_message)
                    _stop(filename, agent)


def _stop(filename, agent):
    """Stop agent.

    Args:
        filename: Filepath of agent to be restarted.
        agent: Agent name

    Returns:
        None

    """
    # Restart
    log_message = (
        'Stopping agent "%s" as it is disabled, but running.'
        '') % (agent)
    log.log2quiet(1033, log_message)
    command2run = ('%s --stop') % (filename)
    _execute(command2run)


def _restart(filename, agent):
    """Restart agent.

    Args:
        filename: Filepath of agent to be restarted.
        agent: Agent name

    Returns:
        None

    """
    # Restart
    log_message = (
        'Starting agent "%s" as it is enabled, but stopped.'
        '') % (agent)
    log.log2quiet(1077, log_message)
    command2run = ('%s --start') % (filename)
    _execute(command2run)


def _execute(command):
    """Run command on CLI.

    Args:
        command: Command to run
        agent: Agent name

    Returns:
        None

    """
    # Run command
    subprocess.run(command.split())
