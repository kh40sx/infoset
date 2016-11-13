"""Infoset Python 3 snmp inventory system.

This package reports and tabulates the status of network connected devices
using snmp queries.

Example:
    TODO add example of using infoset here

"""

from flask import Flask, url_for
from datetime import timedelta
import os
from infoset.utils import Config

# Initializes the Flask Object
infoset = Flask(__name__)

# Function to easily find your assests
infoset.jinja_env.globals['static'] = (
    lambda filename: url_for('static', filename=filename)
)
from www import views

__all__ = ('interfaces', 'snmp', 'web', 'utils')
