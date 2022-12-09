"""
test_dialog
~~~~~~~~~~~

Unit tests for the `thurible.dialog` module.
"""
import unittest as ut

from blessed.keyboard import Keystroke

from thurible import dialog
from tests import test_panel as tp


# Common data.
term = tp.term
KEY_ENTER = Keystroke('\n', term.KEY_ENTER, 'KEY_ENTER')
KEY_LEFT = Keystroke('\x1b[D', term.KEY_LEFT, 'KEY_LEFT')
KEY_RIGHT = Keystroke('\x1b[C', term.KEY_RIGHT, 'KEY_RIGHT')
KEY_Y = Keystroke('y')


# Test cases.
class DialogTestCase(tp.TerminalTestCase):
    def test___init__optional_parameters(self):
        """Given any parameters, a TitlePanel should return an
        object with the expected attributes set.
        """
        # Expected values.
        exp = {
            'message_text': 'spam',
            'options': [
                dialog.Option('Eggs', 'e'),
                dialog.Option('Bacon', 'b'),
            ],
            **tp.kwargs_content_opt_default,
            **tp.kwargs_title_opt_set,
            **tp.kwargs_frame_opt_set,
            **tp.kwargs_panel_req,
            **tp.kwargs_panel_opt_set,
        }

        # Run test.
        d = dialog.Dialog(**exp)

        # Gather actuals.
        act = {key: getattr(d, key) for key in exp}

        # Determine test results.
        self.assertDictEqual(exp, act)

    def test___init__required_parameters(self):
        """Given only the required parameters, a TitlePanel should
        return an object with the expected attributes set.
        """
        # Expected values.
        exp_req = {
            'message_text': 'spam',
            **tp.kwargs_panel_req
        }
        exp_opt = {
            'options': dialog.yes_no,
            **tp.kwargs_content_opt_default,
            **tp.kwargs_title_opt_default,
            **tp.kwargs_frame_opt_default,
            **tp.kwargs_panel_opt_default,
        }

        # Run test.
        d = dialog.Dialog(**exp_req)

        # Gather actuals.
        act_req = {key: getattr(d, key) for key in exp_req}
        act_opt = {key: getattr(d, key) for key in exp_opt}

        # Determine test results.
        self.assertDictEqual(exp_req, act_req)
        self.assertDictEqual(exp_opt, act_opt)

    def test___str__(self):
        """When converted to a string, a Dialog object returns a string
        that will draw the dialog.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}          '
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(4, 0)}          '
            f'{term.move(2, 0)}spam'
            f'{term.reverse}'
            f'{term.move(4, 6)}[No]'
            f'{term.normal}'
            f'{term.move(4, 0)}[Yes]'
        )

        # Test data and state.
        kwargs = {
            'message_text': 'spam',
            'height': 5,
            'width': 10,
        }
        d = dialog.Dialog(**kwargs)

        # Run test.
        act = str(d)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__message_wraps(self):
        """When converted to a string, a Dialog object returns a string
        that will draw the dialog. If the message is longer than the
        width of the Dialog, the message text wraps to the next line.
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
            f'{term.reverse}'
            f'{term.move(4, 6)}[No]'
            f'{term.normal}'
            f'{term.move(4, 0)}[Yes]'
        )

        # Test data and state.
        kwargs = {
            'message_text': 'spam eggs bacon',
            'height': 5,
            'width': 10,
        }
        d = dialog.Dialog(**kwargs)

        # Run test.
        act = str(d)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_enter(self):
        """When a enter is received, `Dialog.action()` should return
        the name of the option selected.
        """
        # Expected values.
        exp = ('No', '')

        # Test data and state.
        kwargs = {
            'message_text': 'spam',
            'height': 5,
            'width': 10,
        }
        d = dialog.Dialog(**kwargs)
        key = KEY_ENTER

        # Run test.
        act = d.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_hot_key(self):
        """When a hot key is received, `Dialog.action()` should move
        the selection to the option assigned to the hot key.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(4, 6)}[No]'
            f'{term.reverse}'
            f'{term.move(4, 0)}[Yes]'
            f'{term.normal}'
        ))

        # Test data and state.
        kwargs = {
            'message_text': 'spam',
            'height': 5,
            'width': 10,
        }
        d = dialog.Dialog(**kwargs)
        key = KEY_Y

        # Run test.
        act = d.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_left_arrow(self):
        """When a left arrow is received, `Dialog.action()` should move
        the selection to the next option to the left of the current
        selection.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(4, 6)}[No]'
            f'{term.reverse}'
            f'{term.move(4, 0)}[Yes]'
            f'{term.normal}'
        ))

        # Test data and state.
        kwargs = {
            'message_text': 'spam',
            'height': 5,
            'width': 10,
        }
        d = dialog.Dialog(**kwargs)
        key = KEY_LEFT

        # Run test.
        act = d.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_left_arrow_at_far_left(self):
        """When a left arrow is received, `Dialog.action()` should move
        the selection to the next option to the left of the current
        selection. If the selection is already at the left-most option,
        the selection should not move.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(4, 6)}[No]'
            f'{term.reverse}'
            f'{term.move(4, 0)}[Yes]'
            f'{term.normal}'
        ))

        # Test data and state.
        kwargs = {
            'message_text': 'spam',
            'height': 5,
            'width': 10,
        }
        d = dialog.Dialog(**kwargs)
        d._selected = 0
        key = KEY_LEFT

        # Run test.
        act = d.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_right_arrow(self):
        """When a right arrow is received, `Dialog.action()` should
        move the selection to the next option to the left of the
        current selection.
        """
        # Expected values.
        exp = ('', (
            f'{term.reverse}'
            f'{term.move(4, 6)}[No]'
            f'{term.normal}'
            f'{term.move(4, 0)}[Yes]'
        ))

        # Test data and state.
        kwargs = {
            'message_text': 'spam',
            'height': 5,
            'width': 10,
        }
        d = dialog.Dialog(**kwargs)
        d._selected = 0
        key = KEY_RIGHT

        # Run test.
        act = d.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_right_arrow_at_far_right(self):
        """When a right arrow is received, `Dialog.action()` should
        move the selection to the next option to the left of the
        current selection. If the selection is already at the
        right-most option, the selection should not move.
        """
        # Expected values.
        exp = ('', (
            f'{term.reverse}'
            f'{term.move(4, 6)}[No]'
            f'{term.normal}'
            f'{term.move(4, 0)}[Yes]'
        ))

        # Test data and state.
        kwargs = {
            'message_text': 'spam',
            'height': 5,
            'width': 10,
        }
        d = dialog.Dialog(**kwargs)
        d._selected = len(dialog.yes_no) - 1
        key = KEY_RIGHT

        # Run test.
        act = d.action(key)

        # Determine test result.
        self.assertEqual(exp, act)
