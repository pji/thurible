"""
test_init
~~~~~~~~~

Unit tests for the initiation of the `thurible` module.
"""
import unittest as ut

import thurible.__init__ as init


# Test case.
class InitTestCase(ut.TestCase):
    def test_get_terminal_stores_terminal(self):
        """When called multiple times, `get_terminal()` will return the
        same instance of `blessed.Terminal` rather than creating a new
        instance.
        """
        # Expected value.
        exp = init.get_terminal()

        # Run test.
        act = init.get_terminal()

        # Determine test result.
        self.assertEqual(exp, act)
