"""Infoset Python 3 snmp inventory system.

This package reports and tabulates the status of network connected devices
using snmp queries.

Example:
    TODO add example of using infoset here

"""

from flask import Flask, url_for
from celery import Celery
from datetime import timedelta
import os


def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


infoset = Flask(__name__)
infoset.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_BACKEND='redis://localhost:6379',
)

infoset.config.update(
    SNMP_CONFIG='infoset/etc'
)
celery = make_celery(infoset)

# Determines the destination of the build
# Only useful if you're using Frozen-Flask
infoset.config['FREEZER_DESTINATION'] = \
    os.path.dirname(os.path.abspath(__file__)) + '/../build'

# Function to easily find your assests
infoset.jinja_env.globals['static'] = (
    lambda filename: url_for('static', filename=filename)
)
from www import views

__all__ = ('interfaces', 'snmp', 'web', 'utils')
