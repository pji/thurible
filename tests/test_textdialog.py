"""
test_textdialog
~~~~~~~~~~~~~~~

Unit tests for the `thurible.textdialog` module.
"""
import unittest as ut

from blessed.keyboard import Keystroke

from thurible import textdialog
from tests import test_panel as tp


# Common data.
term = tp.term
KEY_BACKSPACE = Keystroke('\x08', term.KEY_ENTER, 'KEY_BACKSPACE')
KEY_ENTER = Keystroke('\n', term.KEY_ENTER, 'KEY_ENTER')
KEY_LEFT = Keystroke('\x1b[D', term.KEY_LEFT, 'KEY_LEFT')
KEY_RIGHT = Keystroke('\x1b[C', term.KEY_RIGHT, 'KEY_RIGHT')
KEY_S = Keystroke('s')


# Test class.
class TextDialogTestCase(tp.TerminalTestCase):
    def test___init__optional_parameters(self):
        """Given any parameters, a `TextDialong` should return an
        object with the expected attributes set.
        """
        # Expected values.
        exp = {
            'message_text': 'spam',
            **tp.kwargs_content_opt_default,
            **tp.kwargs_title_opt_set,
            **tp.kwargs_frame_opt_set,
            **tp.kwargs_panel_req,
            **tp.kwargs_panel_opt_set,
        }

        # Run test.
        d = textdialog.TextDialog(**exp)

        # Gather actuals.
        act = {key: getattr(d, key) for key in exp}

        # Determine test results.
        self.assertDictEqual(exp, act)

    def test___init__required_parameters(self):
        """Given only the required parameters, a `TextDialog` should
        return an object with the expected attributes set.
        """
        # Expected values.
        exp_req = {
            'message_text': 'spam',
            **tp.kwargs_panel_req
        }
        exp_opt = {
            **tp.kwargs_content_opt_default,
            **tp.kwargs_title_opt_default,
            **tp.kwargs_frame_opt_default,
            **tp.kwargs_panel_opt_default,
        }

        # Run test.
        d = textdialog.TextDialog(**exp_req)

        # Gather actuals.
        act_req = {key: getattr(d, key) for key in exp_req}
        act_opt = {key: getattr(d, key) for key in exp_opt}

        # Determine test results.
        self.assertDictEqual(exp_req, act_req)
        self.assertDictEqual(exp_opt, act_opt)

    def test___str__(self):
        """When converted to a string, a `TextDialog` object returns a
        string that will draw the dialog.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}          '
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(4, 0)}          '
            f'{term.move(2, 0)}spam'
            f'{term.move(4, 0)}>'
            f'{term.reverse}'
            f'{term.move(4, 2)} '
            f'{term.normal}'
        )

        # Test data and state.
        kwargs = {
            'message_text': 'spam',
            'height': 5,
            'width': 10,
        }
        d = textdialog.TextDialog(**kwargs)

        # Run test.
        act = str(d)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_backspace(self):
        """When a backspace is received, `TextDialog.action()` should
        return the previously entered text as data.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(4, 2)}s       '
            f'{term.reverse}'
            f'{term.move(4, 3)} '
            f'{term.normal}'
        ))

        # Test data and state.
        kwargs = {
            'message_text': 'spam',
            'height': 5,
            'width': 10,
        }
        d = textdialog.TextDialog(**kwargs)
        d.value = 'ss'
        d._selected = 2
        key = KEY_BACKSPACE

        # Run test.
        act = d.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_enter(self):
        """When an enter is received, `TextDialog.action()` should
        return the previously entered text as data.
        """
        # Expected values.
        exp = ('eggs', '')

        # Test data and state.
        kwargs = {
            'message_text': 'spam',
            'height': 5,
            'width': 10,
        }
        d = textdialog.TextDialog(**kwargs)
        d.value = 'eggs'
        key = KEY_ENTER

        # Run test.
        act = d.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_left_arrow(self):
        """When a left arrow is received, `TextDialog.action()` should
        move the cursor to the previous character.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(4, 2)}ss      '
            f'{term.reverse}'
            f'{term.move(4, 3)}s'
            f'{term.normal}'
        ))

        # Test data and state.
        kwargs = {
            'message_text': 'spam',
            'height': 5,
            'width': 10,
        }
        d = textdialog.TextDialog(**kwargs)
        d.value = 'ss'
        d._selected = 2
        key = KEY_LEFT

        # Run test.
        act = d.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_right_arrow(self):
        """When a right arrow is received, `TextDialog.action()` should
        move the cursor to the next character.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(4, 2)}ss      '
            f'{term.reverse}'
            f'{term.move(4, 3)}s'
            f'{term.normal}'
        ))

        # Test data and state.
        kwargs = {
            'message_text': 'spam',
            'height': 5,
            'width': 10,
        }
        d = textdialog.TextDialog(**kwargs)
        d.value = 'ss'
        d._selected = 0
        key = KEY_RIGHT

        # Run test.
        act = d.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_s(self):
        """When an `s` is received, `TextDialog.action()` should update
        the text entry area to include the `s` and move the cursor one
        column to the right.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(4, 2)}s       '
            f'{term.reverse}'
            f'{term.move(4, 3)} '
            f'{term.normal}'
        ))

        # Test data and state.
        kwargs = {
            'message_text': 'spam',
            'height': 5,
            'width': 10,
        }
        d = textdialog.TextDialog(**kwargs)
        d._selected = 0
        key = KEY_S

        # Run test.
        act = d.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_s_with_value(self):
        """When an `s` is received, `TextDialog.action()` should update
        the text entry area to include the `s` and move the cursor one
        column to the right.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(4, 2)}ss      '
            f'{term.reverse}'
            f'{term.move(4, 4)} '
            f'{term.normal}'
        ))

        # Test data and state.
        kwargs = {
            'message_text': 'spam',
            'height': 5,
            'width': 10,
        }
        d = textdialog.TextDialog(**kwargs)
        d._selected = 1
        d.value = 's'
        key = KEY_S

        # Run test.
        act = d.action(key)

        # Determine test result.
        self.assertEqual(exp, act)
