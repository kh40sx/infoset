"""Infoset Python 3 snmp inventory system.

This package reports and tabulates the status of network connected devices
using snmp queries.

Example:
    TODO add example of using infoset here

"""

from flask import Flask, url_for
from flask_restful import Resource, Api
import os

infoset = Flask(__name__)
api = Api(infoset)

# Determines the destination of the build
# Only useful if you're using Frozen-Flask
infoset.config['FREEZER_DESTINATION'] = \
        os.path.dirname(os.path.abspath(__file__))+'/../build'

# Function to easily find your assests
infoset.jinja_env.globals['static'] = (
        lambda filename: url_for('static', filename=filename)
        )
from www import views
__all__ = ('interfaces', 'snmp', 'web', 'utils')
