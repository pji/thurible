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
KEY_BELL = Keystroke('\x07')
KEY_DELETE = Keystroke('\x1b[3~', term.KEY_DELETE, 'KEY_DELETE')
KEY_END = Keystroke('\x1b[F', term.KEY_END, 'KEY_END')
KEY_ENTER = Keystroke('\n', term.KEY_ENTER, 'KEY_ENTER')
KEY_F1 = Keystroke('\x1bOP', term.KEY_F1, 'KEY_F1')
KEY_HOME = Keystroke('\x1b[H', term.KEY_HOME, 'KEY_HOME')
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
            f'{term.move(4, 0)}> '
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

    def test___str__message_wraps(self):
        """When converted to a string, a `TextDialog` object returns a
        string that will draw the dialog. If the message is longer than
        the width of the Dialog, the message text wraps to the next line.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}          '
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(4, 0)}          '
            f'{term.move(1, 0)}spam eggs'
            f'{term.move(2, 0)}bacon'
            f'{term.move(4, 0)}> '
            f'{term.reverse}'
            f'{term.move(4, 2)} '
            f'{term.normal}'
        )

        # Test data and state.
        kwargs = {
            'message_text': 'spam eggs bacon',
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
        delete the previous character.
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

    def test_action_delete(self):
        """When a delete is received, `TextDialog.action()` should
        delete the selected character.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(4, 2)}am      '
            f'{term.reverse}'
            f'{term.move(4, 2)}a'
            f'{term.normal}'
        ))

        # Test data and state.
        kwargs = {
            'message_text': 'spam',
            'height': 5,
            'width': 10,
        }
        d = textdialog.TextDialog(**kwargs)
        d.value = 'ham'
        d._selected = 0
        key = KEY_DELETE

        # Run test.
        act = d.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_end(self):
        """When an end is received, `TextDialog.action()` should
        move the cursor to the last position.
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
        d.value = 'ss'
        d._selected = 0
        key = KEY_END

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

    def test_action_home(self):
        """When a home is received, `TextDialog.action()` should
        move the cursor to the first character.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(4, 2)}ss      '
            f'{term.reverse}'
            f'{term.move(4, 2)}s'
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
        key = KEY_HOME

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

    def test_action_left_arrow_cannot_go_past_home(self):
        """When a left arrow is received, `TextDialog.action()` should
        move the cursor to the previous character. If at the left-most
        character, the cursor cannot move to a previous character.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(4, 2)}ss      '
            f'{term.reverse}'
            f'{term.move(4, 2)}s'
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
        key = KEY_LEFT

        # Run test.
        act = d.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_not_a_keystroke(self):
        """When something other than a keystroke is received,
        `TextDialog.action()` should throw a ValueError exception.
        """
        # Expected values.
        exp_ex = ValueError
        exp_msg = 'Can only accept Keystrokes. Received: str.'

        # Test data and state.
        kwargs = {
            'message_text': 'spam',
            'height': 5,
            'width': 10,
        }
        d = textdialog.TextDialog(**kwargs)
        key = '\x00'

        # Run test and determine results.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            act = d.action(key)

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

    def test_action_right_arrow_cannot_go_past_end(self):
        """When a right arrow is received, `TextDialog.action()` should
        move the cursor to the next character. If the cursor is in the
        right-most position, the cursor cannot move to the right.
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
        d.value = 'ss'
        d._selected = 2
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

    def test_action_s_with_value_inserting_character(self):
        """When an `s` is received, `TextDialog.action()` should update
        the text entry area to include the `s` and move the cursor one
        column to the right. If the cursor has selected a character in
        the value, the typed character is inserted before the selected
        character.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(4, 2)}asa     '
            f'{term.reverse}'
            f'{term.move(4, 4)}a'
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
        d.value = 'aa'
        key = KEY_S

        # Run test.
        act = d.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_undefined_application_key(self):
        """When an "application" keystroke whose behavior has not been
        defined is received, `TextDialog.action()` should return the
        string value of the keystroke as data.
        """
        # Expected values.
        exp = ('\x1bOP', '')

        # Test data and state.
        kwargs = {
            'message_text': 'spam',
            'height': 5,
            'width': 10,
        }
        d = textdialog.TextDialog(**kwargs)
        d.value = 'eggs'
        key = KEY_F1

        # Run test.
        act = d.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_undefined_control_key(self):
        """When a control character keystroke whose behavior has not
        been defined is received, `TextDialog.action()` should return
        the string value of the keystroke as data.
        """
        # Expected values.
        exp = ('\x07', '')

        # Test data and state.
        kwargs = {
            'message_text': 'spam',
            'height': 5,
            'width': 10,
        }
        d = textdialog.TextDialog(**kwargs)
        d.value = 'eggs'
        key = KEY_BELL

        # Run test.
        act = d.action(key)

        # Determine test result.
        self.assertEqual(exp, act)
