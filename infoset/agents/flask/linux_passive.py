#!/usr/bin/env python3
"""This is a test of flask."""

import os
import socket
import json
from flask import Flask, request
from pprint import pprint
import logging

from infoset.agents import agent as Agent
from infoset.agents import data_linux
from infoset.utils import jm_configuration

# Define flask parameters
APP = Flask(__name__)


@APP.route('/')
def home():
    """Display api data on home page.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    agent_name = 'linux_passive'

    # Get configuration
    config_dir = os.environ['INFOSET_CONFIGDIR']
    config = jm_configuration.ConfigAgent(
        config_dir, agent_name)

    # Get hostname
    hostname = socket.getfqdn()

    # Get the UID for the agent
    uid = Agent.get_uid(hostname)

    # Initialize key variables
    agent = Agent.Agent(uid, config, hostname)

    # Update agent with linux data
    data_linux.getall(agent)

    # Return
    data_dict = agent.polled_data()
    data = json.dumps(data_dict)
    return data

def infoset_logging():
    """Format logging for the application.

    Args:
        None

    Returns:
        handler: Logging handler for application

    """
    # Get log file
    config = jm_configuration.ConfigCommon(os.environ['INFOSET_CONFIGDIR'])
    web_log_file = config.web_log_file()

    # Format the logging
    log_format = (
        '%(asctime)s - n=%(name)s - '
        'l=%(levelname)s - msg=%(message)s - '
        'u=%(user_id)s - ip=%(ip)s - m=%(method)s - '
        'url=%(url)s - msg=%(message)s url=%(url)s')
    formatter = logging.Formatter(log_format)

    # Populate the logging handler
    handler = logging.FileHandler(filename=web_log_file)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    # Return
    return handler


if __name__ == "__main__":
    APP.logger.setLevel(logging.DEBUG)
    APP.logger.addHandler(infoset_logging())

    # Start app
    APP.run(debug=True)
