"""
test_util
~~~~~~~~~

Unit tests for the `thurible.util` module.
"""
import unittest as ut

from thurible import util


class FrameTestCase(ut.TestCase):
    def test_normal(self):
        "A Box object should return box characters."""
        # Expected value.
        expected = {
            'top': '\u2500',
            'bot': '\u2500',
            'side': '\u2502',
            'ltop': '\u250c',
            'rtop': '\u2510',
            'mtop': '\u252c',
            'lbot': '\u2514',
            'rbot': '\u2518',
            'mbot': '\u2534',
            'lside': '\u251c',
            'rside': '\u2524',
            'mid': '\u253c',
        }

        # Test data and state.
        box = util.Frame()

        # Run test and gather actuals.
        for attr in expected:
            actual = getattr(box, attr)

            # Determine test result.
            self.assertEqual(expected[attr], actual)

    def test_change_type(self):
        """If given a kind, the kind property should change the kind
        attribute and the _chars attribute.
        """
        # Expected value.
        expected = ['\u2500', '\u2501', '\u2508']

        # Test data and state.
        box = util.Frame('light')

        # Run test and gather actuals.
        actual = [box.top,]
        box.kind = 'heavy'
        actual.append(box.top)
        box.kind = 'light_quadruple_dash'
        actual.append(box.top)

        # Determine test result.
        self.assertEqual(expected, actual)

    def test_custom(self):
        """If given a kind of 'custom' string of characters, the box
         object should return the custom characters and it's kind
         should be 'custom'.
        """
        # Expected value.
        exp_kind = 'custom'
        exp_chars = 'abcdefghijklmn'
        exp_sample = 'g'

        # Test data and state.
        box = util.Frame(custom=exp_chars)

        # Run test and gather actuals.
        act_kind = box.kind
        act_chars = box._chars
        act_sample = box.mtop

        # Determine test result.
        self.assertEqual(exp_kind, act_kind)
        self.assertEqual(exp_chars, act_chars)
        self.assertEqual(exp_sample, act_sample)

    def test_invalid_custom_string(self):
        """The passed custom string is not exactly fourteen characters
        long, a ValueError should be raised.
        """
        # Expected value.
        expected = ValueError

        # Run test and determine result.
        with self.assertRaises(expected):
            box = util.Frame(custom='bad')
