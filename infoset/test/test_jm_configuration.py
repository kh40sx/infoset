#!/usr/bin/env python3
"""Test the jm_configuration module."""

import os
import os.path
import unittest
import shutil
import random
import string
import hashlib
import tempfile
import yaml
from infoset.utils import jm_configuration as test_class


class TestConfig(unittest.TestCase):
    """Checks all functions and methods."""

    # ---------------------------------------------------------------------- #
    # General object setup
    # ---------------------------------------------------------------------- #

    # Required
    maxDiff = None

    random_string = ''.join([random.choice(
        string.ascii_letters + string.digits) for n in range(9)])

    @classmethod
    def setUpClass(cls):
        # Initializing key variables
        hash_object = hashlib.sha256(b'%s')
        hexvalue = hash_object.hexdigest()

        configuration = (
            """
            log_file: /tmp/%s/Vupstrr79LdeYuVD/infoset.log
            web_directory: /tmp/%s/HMSLAa65d8D2qwEu
            data_directory: /tmp/%s/6maYNHCVZyQ9yJFm/data
            ingest_cache_directory: /tmp/%s/p9ZuZrRzWAd8GeSc
            poller_threads: 20
            ingest_threads: 20
            db_hostname: localhost_TEST
            db_username: Qc5QRNkkgQzcWUEF
            db_password: P8jsCuVH2krrVdqQ
            db_name: 5xjyjPAwPNmGsY3Z
            hosts:
                - 192.168.1.1
                - 192.168.1.2
                - 192.168.1.3
                - 192.168.1.4
            """) % (hexvalue, hexvalue, hexvalue, hexvalue)

        cls.test_root_directory = ('/tmp/%s/') % (hexvalue)
        cls.configuration_dict = yaml.load(configuration)

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
        cls.testobj = test_class.Config(cls.tmpdir)

    @classmethod
    def tearDownClass(cls):
        # Cleanup temporary files when done
        shutil.rmtree(cls.tmpdir)
        shutil.rmtree(cls.test_root_directory)

    def test_data_directory(self):
        """Testing method / function data_directory."""
        # Initializing key variables
        # Fails because directory doesn't exist
        with self.assertRaises(SystemExit):
            self.testobj.data_directory()

        # Doesn't fail because directory now exists
        os.makedirs(self.configuration_dict['data_directory'])
        result = self.testobj.data_directory()
        expected = self.configuration_dict['data_directory']
        self.assertEqual(result, expected)

    def test_web_directory(self):
        """Testing method / function web_directory."""
        # Initializing key variables
        # Fails because directory doesn't exist
        with self.assertRaises(SystemExit):
            self.testobj.web_directory()

        # Doesn't fail because directory now exists
        os.makedirs(self.configuration_dict['web_directory'])
        result = self.testobj.web_directory()
        expected = self.configuration_dict['web_directory']
        self.assertEqual(result, expected)

    def test_snmp_directory(self):
        """Testing method / function snmp_directory."""
        # Initializing key variables
        # Verify that directory exists
        result = self.testobj.snmp_directory()
        self.assertEqual(os.path.exists(result), True)
        self.assertEqual(os.path.isdir(result), True)

        # Doesn't fail because directory now exists
        result = self.testobj.snmp_directory()
        expected = ('%s/snmp') % (self.configuration_dict['data_directory'])
        self.assertEqual(result, expected)

    def test_snmp_device_file(self):
        """Testing method / function snmp_device_file."""
        # Initializing key variables
        # Doesn't fail because directory now exists
        result = self.testobj.snmp_device_file(self.random_string)
        expected = ('%s/%s.yaml') % (
            self.testobj.snmp_directory(), self.random_string)
        self.assertEqual(result, expected)

    def test_ingest_cache_directory(self):
        """Testing method / function ingest_cache_directory."""
        # Initializing key variables
        # Fails because directory doesn't exist
        with self.assertRaises(SystemExit):
            self.testobj.ingest_cache_directory()

        # Doesn't fail because directory now exists
        os.makedirs(self.configuration_dict['ingest_cache_directory'])
        result = self.testobj.ingest_cache_directory()
        expected = self.configuration_dict['ingest_cache_directory']
        self.assertEqual(result, expected)

    def test_db_name(self):
        """Testing for db_name."""
        # Initializing key variables
        result = self.testobj.db_name()
        expected = self.configuration_dict['db_name']
        self.assertEqual(result, expected)

    def test_db_username(self):
        """Testing for db_username."""
        # Initializing key variables
        result = self.testobj.db_username()
        expected = self.configuration_dict['db_username']
        self.assertEqual(result, expected)

    def test_db_password(self):
        """Testing for db_password."""
        # Initializing key variables
        result = self.testobj.db_password()
        expected = self.configuration_dict['db_password']
        self.assertEqual(result, expected)

    def test_db_hostname(self):
        """Testing for db_hostname."""
        # Initializing key variables
        result = self.testobj.db_hostname()
        expected = self.configuration_dict['db_hostname']
        self.assertEqual(result, expected)

    def test_ingest_threads(self):
        """Testing for ingest_threads."""
        # Initializing key variables
        result = self.testobj.ingest_threads()
        expected = self.configuration_dict['ingest_threads']
        self.assertEqual(result, expected)

    def test_log_file(self):
        """Testing for log_file."""
        # Initializing key variables
        result = self.testobj.log_file()
        expected = self.configuration_dict['log_file']
        self.assertEqual(result, expected)

    def test_hosts(self):
        """Testing for hosts."""
        # Initializing key variables
        result = self.testobj.hosts()
        expected = self.configuration_dict['hosts']
        self.assertEqual(result, expected)


class TestConfigAgent(unittest.TestCase):
    """Checks configuration information."""

    # ---------------------------------------------------------------------- #
    # General object setup
    # ---------------------------------------------------------------------- #

    # Required
    maxDiff = None

    random_string = ''.join([random.choice(
        string.ascii_letters + string.digits) for n in range(9)])

    @classmethod
    def setUpClass(cls):
        # Initializing key variables
        hash_object = hashlib.sha256(b'%s')
        hexvalue = hash_object.hexdigest()

        configuration = (
            """
            log_file: /tmp/%s/Vupstrr79LdeYuVD/infoset.log
            server_name: 192.168.1.218
            server_port: 5000
            server_https: False
            agent_cache_directory: /tmp/%s/778E9u5WJsYd7Ab3/age_cache
            agent_source_descriptions:
                Sentry3_infeedPower: Input Power Per Phase
                Sentry3_infeedLoadValue: Input Current Per Phase
                Sentry3_infeedName: Input Power Phase Name
                Sentry3_Sentry3_infeedID: Input Power Phase ID
            agent_snmp_hostnames:
                - 192.168.1.254
            """) % (hexvalue, hexvalue)

        cls.test_root_directory = ('/tmp/%s/') % (hexvalue)
        cls.configuration_dict = yaml.load(configuration)
        cls.name = '8E9u5WJsYd7'

        # Create temporary configuration file
        cls.tmpdir = tempfile.mkdtemp()

        # Make relevant sub directories
        subdirectories = ['agents', 'common']
        for subdirectory in subdirectories:
            directory = ('%s/%s') % (cls.tmpdir, subdirectory)
            os.mkdir(directory)
            tmpfile = ('%s/config.yaml') % (directory)
            with open(tmpfile, 'w') as f_handle:
                f_handle.write(configuration)
        # Create a subdirectory for the agent under agents/
        os.mkdir(
            ('%s/agents/%s') % (cls.tmpdir, cls.name))

        # Instantiate object to test
        cls.testobj = test_class.ConfigAgent(cls.tmpdir, cls.name)

    @classmethod
    def tearDownClass(cls):
        # Cleanup temporary files when done
        shutil.rmtree(cls.tmpdir)
        shutil.rmtree(cls.test_root_directory)

    def test_log_file(self):
        """Testing for log_file."""
        # Initializing key variables
        result = self.testobj.log_file()
        expected = self.configuration_dict['log_file']
        self.assertEqual(result, expected)

    def test_server_name(self):
        """Testing for server_name."""
        # Initializing key variables
        result = self.testobj.server_name()
        expected = self.configuration_dict['server_name']
        self.assertEqual(result, expected)

    def test_server_port(self):
        """Testing for server_port."""
        # Initializing key variables
        result = self.testobj.server_port()
        expected = self.configuration_dict['server_port']
        self.assertEqual(result, expected)

    def test_server_https(self):
        """Testing for server_https."""
        # Initializing key variables
        result = self.testobj.server_https()
        expected = self.configuration_dict['server_https']
        self.assertEqual(result, expected)

    def test_agent_name(self):
        """Testing for agent_name."""
        # Fails because directory doesn't exist
        expected = self.name
        result = self.testobj.agent_name()
        self.assertEqual(result, expected)

    def test_agent_cache_directory(self):
        """Testing method / function agent_cache_directory."""
        # Initializing key variables
        # Fails because directory doesn't exist
        with self.assertRaises(SystemExit):
            self.testobj.agent_cache_directory()

        # Doesn't fail because directory now exists
        os.makedirs(self.configuration_dict['agent_cache_directory'])
        result = self.testobj.agent_cache_directory()
        expected = self.configuration_dict['agent_cache_directory']
        self.assertEqual(result, expected)

    def test_agent_snmp_hostnames(self):
        """Testing for agent_snmp_hostnames."""
        # Initializing key variables
        result = self.testobj.agent_snmp_hostnames()
        expected = self.configuration_dict['agent_snmp_hostnames']
        self.assertEqual(result, expected)


class TestConfigSNMP(unittest.TestCase):
    """Checks all functions and methods."""

    # ---------------------------------------------------------------------- #
    # General object setup
    # ---------------------------------------------------------------------- #

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
