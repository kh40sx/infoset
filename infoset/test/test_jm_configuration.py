#!/usr/bin/env python3
"""Test the jm_configuration module."""

import os
import unittest
import shutil
import random
import string
import tempfile

from infoset.utils import jm_configuration as test_class


class TestConfigServer(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Required
    maxDiff = None

    random_string = ''.join([random.choice(
        string.ascii_letters + string.digits) for n in range(9)])

    @classmethod
    def setUpClass(cls):
        # Initializing key variables
        configuration = """
web_directory: /tmp
data_directory: /tmp
"""
        # Create temporary configuration file
        cls.tmpdir = tempfile.mkdtemp()

        # Make relevant sub directories
        subdirectories = ['server', 'common']
        for subdirectory in subdirectories:
            directory = ('%s/%s') % (cls.tmpdir, subdirectory)
            os.mkdir(directory)
            tmpfile = ('%s/config.yaml') % (directory)
            with open(tmpfile, 'w') as f_handle:
                f_handle.write(configuration)

        # Instantiate object to test
        cls.testobj = test_class.ConfigServer(cls.tmpdir)

    @classmethod
    def tearDownClass(cls):
        # Cleanup temporary files when done
        shutil.rmtree(cls.tmpdir)

    def test_data_directory(self):
        """Testing method / function data_directory."""
        # Initializing key variables
        result = self.testobj.data_directory()
        expected = '/tmp'
        self.assertEqual(result, expected)

    def test_web_directory(self):
        """Testing method / function web_directory."""
        # Initializing key variables
        result = self.testobj.web_directory()
        expected = '/tmp'
        self.assertEqual(result, expected)

    def test_snmp_directory(self):
        """Testing method / function snmp_directory."""
        # Initializing key variables
        result = self.testobj.snmp_directory()
        expected = ('%s/snmp') % (self.testobj.data_directory())
        self.assertEqual(result, expected)

    def test_snmp_device_file(self):
        """Testing method / function snmp_device_file."""
        # Initializing key variables
        result = self.testobj.snmp_device_file(self.random_string)
        expected = ('%s/%s.yaml') % (
            self.testobj.snmp_directory(), self.random_string)
        self.assertEqual(result, expected)


class TestConfigSNMP(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Required
    maxDiff = None

    random_string = ''.join([random.choice(
        string.ascii_letters + string.digits) for n in range(9)])

    @classmethod
    def setUpClass(cls):
        # Initializing key variables
        configuration = """
snmp_groups:
    - group_name: Corporate Campus
      snmp_version: 3
      snmp_secname: woohoo
      snmp_community:
      snmp_port: 161
      snmp_authprotocol: sha
      snmp_authpassword: auth123
      snmp_privprotocol: des
      snmp_privpassword: priv123

    - group_name: Remote Sites
      snmp_version: 3
      snmp_secname: foobar
      snmp_community:
      snmp_port: 161
      snmp_authprotocol: sha
      snmp_authpassword: 123auth
      snmp_privprotocol: aes
      snmp_privpassword: 123priv
"""
        # Create temporary configuration file
        cls.tmpdir = tempfile.mkdtemp()

        # Make relevant sub directories
        subdirectories = ['snmp']
        for subdirectory in subdirectories:
            directory = ('%s/%s') % (cls.tmpdir, subdirectory)
            os.mkdir(directory)
            tmpfile = ('%s/config.yaml') % (directory)
            with open(tmpfile, 'w') as f_handle:
                f_handle.write(configuration)

        # Instantiate object to test
        cls.testobj = test_class.ConfigSNMP(cls.tmpdir)

    @classmethod
    def tearDownClass(cls):
        # Cleanup temporary files when done
        shutil.rmtree(cls.tmpdir)

    def test_snmp_auth(self):
        """Testing method / function snmp_auth."""
        # Initializing key variables
        expected_list = [
            {
                'group_name': 'Corporate Campus',
                'snmp_version': 3,
                'snmp_secname': 'woohoo',
                'snmp_community': None,
                'snmp_port': 161,
                'snmp_authprotocol': 'sha',
                'snmp_authpassword': 'auth123',
                'snmp_privprotocol': 'des',
                'snmp_privpassword': 'priv123'
            }, {
                'group_name': 'Remote Sites',
                'snmp_version': 3,
                'snmp_secname': 'foobar',
                'snmp_community': None,
                'snmp_port': 161,
                'snmp_authprotocol': 'sha',
                'snmp_authpassword': '123auth',
                'snmp_privprotocol': 'aes',
                'snmp_privpassword': '123priv'
            }]

        # Do test
        result = self.testobj.snmp_auth()
        for index, result_dict in enumerate(result):
            expected_dict = expected_list[index]
            for key in expected_dict.keys():
                if key.startswith('snmp_'):
                    self.assertEqual(result_dict[key], expected_dict[key])


if __name__ == '__main__':

    # Do the unit test
    unittest.main()
