#!/usr/bin/env python
"""Test the jm_iana_enterprise module."""

import unittest

import jm_iana_enterprise as testimport


class KnownValues(unittest.TestCase):
    """Checks all class_config methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Required
    maxDiff = None

    def enterprise(self):
        """Testing method / function enterprise."""
        # Initializing key variables
        test = testimport(sysobject_id='.1.2.3.4.5.6.100.101.102')
        result = test.enterprise()
        self.assertEqual(result, 100)

    def is_cisco(self):
        """Testing method / function is_cisco."""
        # Test for Cisco sysObjectID
        test = testimport(sysobject_id='.1.2.3.4.5.6.9.101.102')
        result = test.is_cisco()
        self.assertEqual(result, True)

        # Test for fake vendor
        test = testimport(sysobject_id='.1.2.3.4.5.6.100000000000000.101.102')
        result = test.is_cisco()
        self.assertEqual(result, False)

    def is_juniper(self):
        """Testing method / function is_juniper."""
        # Test for Juniper sysObjectID
        test = testimport(sysobject_id='.1.2.3.4.5.6.2636.101.102')
        result = test.is_juniper()
        self.assertEqual(result, True)

        # Test for fake vendor
        test = testimport(sysobject_id='.1.2.3.4.5.6.100000000000000.101.102')
        result = test.is_juniper()
        self.assertEqual(result, False)


if __name__ == '__main__':

    # Do the unit test
    unittest.main()
