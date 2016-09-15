#!/usr/bin/env python3
"""Test the jm_general module."""

import unittest

from infoset.db import db_agent
from infoset.db.db_orm import Agent
from infoset.db import db
from infoset.utils import jm_general


class KnownValues(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Intstantiate a good agent
    idx_agent_good = 1
    idx_agent_malo = -1
    good_agent = db_agent.GetIDX(idx_agent_good)

    # Get agent data using SQLalchemy directly
    database = db.Database()
    session = database.session()
    result = session.query(Agent).filter(
        Agent.idx == idx_agent_good).one()
    session.close()
    good_id = jm_general.decode(result.id)

    def test_uid(self):
        """Testing method / function uid."""
        # Testing with known good value
        expected = self.good_id
        result = self.good_agent.uid()
        self.assertEqual(result, expected)

        # Testing with known bad value
        expected = (
            '8f365c408a8 feb 5  38c726d ba09156486'
            'b837aa6070d 0bba49 0af9cefd')
        result = self.good_agent.uid()
        self.assertNotEqual(result, expected)

        # Test with non existent AgentID
        with self.assertRaises(SystemExit):
            _ = db_agent.GetIDX(self.idx_agent_malo)


if __name__ == '__main__':

    # Do the unit test
    unittest.main()
