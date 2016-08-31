#!/usr/bin/env python3
"""Infoset setup script.

Run this script when setting up for the first time

"""

import os
import sys
from setuptools import setup, find_packages


# Define key files
SETUP_SCRIPT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))

README_FILE = open(
    os.path.join(SETUP_SCRIPT_DIRECTORY, 'README.md')).read()
NEWS_FILE = open(
    os.path.join(SETUP_SCRIPT_DIRECTORY, 'NEWS.txt')).read()

# Define other parameters
VERSION = '0.0.0.0'
PYPI = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
    'astroid >= 1.4.8',
    'click >= 6.6',
    'colorama >= 0.3.7',
    'Flask >= 0.11.1',
    'Flask-RESTful >= 0.3.5',
    'funcsigs >= 1.0.2',
    'isort >= 4.2.5',
    'itsdangerous >= 0.24',
    'Jinja2 >= 2.8',
    'lazy-object-proxy >= 1.2.2',
    'MarkupSafe >= 0.23',
    'mccabe >= 0.5.2',
    'mock >= 2.0.0',
    'nose >= 1.3.7',
    'numpy >= 1.11.1',
    'pbr >= 1.10.0',
    'pep257 >= 0.7.0',
    'pep8 >= 1.7.0',
    'ply >= 3.8',
    'psutil >= 4.3.0',
    'pyasn1 >= 0.1.9',
    'pycrypto >= 2.6.1',
    'pylint >= 1.6.4',
    'PyMySQL >= 0.7.6',
    'pysmi >= 0.0.7',
    'pysnmp >= 4.3.2',
    'python-dateutil >= 2.5.3',
    'pytz >= 2016.6.1',
    'PyYAML >= 3.11',
    'requests >= 2.11.0',
    'six >= 1.10.0',
    'SQLAlchemy >= 1.0.14',
    'Werkzeug >= 0.11.10',
    'wrapt >= 1.10.8'
]

setup(
    name='Infoset',
    version=VERSION,
    description=(
        'System performance charting and network topology system'),
    long_description=README_FILE + '\n\n' + NEWS_FILE,
    classifiers=[
        # Get strings from
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Environment :: Console',
        'Programming Language :: Python :: 3'
    ],
    keywords='infoset snmp switchmap network map',
    author='UWIComputingSociety',
    author_email='',
    url='',
    license='',
    packages=find_packages(
        exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
    scripts=['setup/install/install.py'],
    include_package_data=True,
    zip_safe=False,
    install_requires=PYPI,
    entry_points={
        'console_scripts':
        ['infoset=infoset.toolbox:main']
    }
)
