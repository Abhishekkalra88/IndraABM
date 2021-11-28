"""
Tests for the actions module.
"""

from unittest import TestCase

import lib.actions as acts
import lib.agent as agt
import lib.group as grp

TEST_AGENT = "test agent"


class ActionsTestCase(TestCase):
    def setUp(self):
        # We will just fake an exec key for this agent:
        self.agent = agt.Agent("Test agent", exec_key=None)
        self.agent_for_group = agt.Agent("Test agent for group",
                                          exec_key=None)
        self.group = grp.Group("Test group")

    def tearDown(self):
        self.agent = None

    def test_def_action(self):
        """
        Test our default agent action.
        """
        self.assertEqual(agt.DONT_MOVE, acts.def_action(self.agent))

    def test_create_agent(self):
        self.assertIsInstance(acts.create_agent(TEST_AGENT, 0,
                              exec_key=None),
                              agt.Agent)

    def test_def_action(self):
        """
        Test for default agent.
        """
        self.assertTrue(acts.def_action(self.agent))

    def test_join(self):
        """
        Test join.
        """
        self.assertFalse(self.agent, self.group)
        self.assertTrue(self.group, self.agent)
