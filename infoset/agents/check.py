#!/usr/bin/env python3

"""Demonstration Script that extracts agent data from cache directory files.

This could be a modified to be a daemon

"""

# Standard libraries
import os
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

        # Get agent names
        agents.append(os.path.basename(sub_directory))

    for agent in agents:
        # Get agent status variables
        config = jm_configuration.ConfigAgent(config_directory, agent)
        filename = ('%s/%s') % (root_dir, config.agent_filename())
        pid = hidden.File()
        pidfile = pid.pid(agent)

        # Check for agent existence
        if config.agent_enabled() is True:
            # Ignore agents that cannot be found
            if os.path.isfile(filename) is False:
                log_message = (
                    'Agent executable file %s listed in the '
                    'configuration file '
                    'of agent "%s" does not exist. Please fix.'
                    '') % (config.agent_filename(), agent)
                log.log2quiet(1075, log_message)
                continue

            # Check for pid file
            if os.path.isfile(pidfile) is True:
                with open(pidfile, 'r') as f_handle:
                    pid = int(f_handle.readline().strip())
                if psutil.pid_exists(pid) is False:
                    log_message = (
                        'Agent "%s" is dead. Attempting to restart.'
                        '') % (agent)
                    log.log2quiet(1076, log_message)

                    # Remove PID file and restart
                    os.remove(pidfile)
                    _restart(filename)
            else:
                _restart(filename)


def _restart(filename):
    """Restart agent.

    Args:
        filename: Filepath of agent to be restarted.

    Returns:
        None

    """
    # Restart
    command2run = ('%s --start') % (filename)
    jm_general.run_script(command2run, die=False)
