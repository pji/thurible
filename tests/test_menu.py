"""
test_menu
~~~~~~~~~

Unit tests for the `thurible.menu` module.
"""
import unittest as ut
from unittest.mock import patch

from blessed import Terminal
from blessed.keyboard import Keystroke

from thurible import menu
from tests.test_panel import term, TerminalTestCase
import tests.test_panel as tp


# Common data.
KEY_DOWN = Keystroke('\x1b[B', term.KEY_DOWN, 'KEY_DOWN')
KEY_E = Keystroke('e')
KEY_END = Keystroke('\x1b[F', term.KEY_END, 'KEY_END')
KEY_ENTER = Keystroke('\n', term.KEY_ENTER, 'KEY_ENTER')
KEY_HOME = Keystroke('\x1b[H', term.KEY_HOME, 'KEY_HOME')
KEY_O = Keystroke('o')
KEY_PGDOWN = Keystroke('\x1b[U', term.KEY_PGDOWN, 'KEY_PGDOWN')
KEY_PGUP = Keystroke('\x1b[V', term.KEY_PGUP, 'KEY_PGUP')
KEY_UP = Keystroke('\x1b[A', term.KEY_UP, 'KEY_UP')
KEY_X = Keystroke('x')


# Test case.
class MenuTestCase(TerminalTestCase):
    def test___init__optional_parameters(self):
        """Given any parameters, a Menu should return an
        object with the expected attributes set.
        """
        # Expected values.
        exp = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
            ],
            'option_align_h': 'right',
            'select_bg': 'red',
            'select_fg': 'blue',
            **tp.kwargs_content_opt_default_alt,
            **tp.kwargs_title_opt_set,
            **tp.kwargs_frame_opt_set,
            **tp.kwargs_panel_req,
            **tp.kwargs_panel_opt_set,
        }

        # Run test.
        m = menu.Menu(**exp)

        # Gather actuals.
        act = {key: getattr(m, key) for key in exp}

        # Determine test results.
        self.assertDictEqual(exp, act)

    def test___init__required_parameters(self):
        """Given only the required parameters, a Menu should
        return an object with the expected attributes set.
        """
        # Expected values.
        exp_req = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
            ],
        }
        exp_opt = {
            'select_bg': '',
            'select_fg': '',
            'option_align_h': 'left',
            **tp.kwargs_content_opt_default_alt,
            **tp.kwargs_title_opt_default,
            **tp.kwargs_frame_opt_default,
            **tp.kwargs_panel_opt_default,
        }

        # Run test.
        m = menu.Menu(**exp_req)

        # Gather actuals.
        act_req = {key: getattr(m, key) for key in exp_req}
        act_opt = {key: getattr(m, key) for key in exp_opt}

        # Determine test results.
        self.assertDictEqual(exp_req, act_req)
        self.assertDictEqual(exp_opt, act_opt)

    def test___str__(self):
        """When converted to a string, a Menu object returns a string
        that will draw the entire menu.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}       '
            f'{term.move(1, 0)}       '
            f'{term.move(2, 0)}       '
            f'{term.move(3, 0)}       '
            f'{term.move(4, 0)}       '
            f'{term.reverse}'
            f'{term.move(0, 0)}spam '
            f'{term.normal}'
            f'{term.move(1, 0)}eggs '
            f'{term.move(2, 0)}bacon'
        )

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
            ],
            'height': 5,
            'width': 7,
            'term': term,
        }
        m = menu.Menu(**kwargs)

        # Run test.
        act = str(m)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_bg_and_fg(self):
        """When converted to a string, a Menu object returns a string
        that will draw the entire menu. If foreground or background
        colors are given, the contents of the panel should have those
        colors.
        """
        # Expected values.
        exp = (
            f'{term.red_on_blue}'
            f'{term.move(0, 0)}       '
            f'{term.move(1, 0)}       '
            f'{term.move(2, 0)}       '
            f'{term.move(3, 0)}       '
            f'{term.move(4, 0)}       '
            f'{term.normal}'
            f'{term.red_on_blue}'
            f'{term.reverse}'
            f'{term.move(0, 0)}spam '
            f'{term.normal}'
            f'{term.red_on_blue}'
            f'{term.move(1, 0)}eggs '
            f'{term.move(2, 0)}bacon'
            f'{term.normal}'
        )

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
            ],
            'height': 5,
            'width': 7,
            'term': term,
            'bg': 'blue',
            'fg': 'red',
        }
        m = menu.Menu(**kwargs)

        # Run test.
        act = str(m)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_content_and_option_align_h_center(self):
        """When converted to a string, a Menu object returns a string
        that will draw the entire menu. If the horizontal content
        alignment is centered, the options should be centered within
        the panel.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}         '
            f'{term.move(1, 0)}         '
            f'{term.move(2, 0)}         '
            f'{term.move(3, 0)}         '
            f'{term.move(4, 0)}         '
            f'{term.reverse}'
            f'{term.move(0, 2)}spam '
            f'{term.normal}'
            f'{term.move(1, 2)}eggs '
            f'{term.move(2, 2)}bacon'
            f'{term.move(3, 2)} ham '
        )

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
                menu.Option('ham', 'h'),
            ],
            'option_align_h': 'center',
            'content_align_h': 'center',
            'height': 5,
            'width': 9,
            'term': term,
        }
        m = menu.Menu(**kwargs)

        # Run test.
        act = str(m)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_content_and_option_align_h_right(self):
        """When converted to a string, a Menu object returns a string
        that will draw the entire menu. If the horizontal content
        alignment is right, the options should be right aligned within
        the panel.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}         '
            f'{term.move(1, 0)}         '
            f'{term.move(2, 0)}         '
            f'{term.move(3, 0)}         '
            f'{term.move(4, 0)}         '
            f'{term.reverse}'
            f'{term.move(0, 4)} spam'
            f'{term.normal}'
            f'{term.move(1, 4)} eggs'
            f'{term.move(2, 4)}bacon'
            f'{term.move(3, 4)}  ham'
        )

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
                menu.Option('ham', 'h'),
            ],
            'option_align_h': 'right',
            'content_align_h': 'right',
            'height': 5,
            'width': 9,
            'term': term,
        }
        m = menu.Menu(**kwargs)

        # Run test.
        act = str(m)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_content_pad_left(self):
        """When converted to a string, a Menu object returns a string
        that will draw the entire menu. If left content padding is set,
        the options will be inset by the amount of padding.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}          '
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(4, 0)}          '
            f'{term.reverse}'
            f'{term.move(0, 3)}spam '
            f'{term.normal}'
            f'{term.move(1, 3)}eggs '
            f'{term.move(2, 3)}bacon'
        )

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
            ],
            'content_pad_left': 0.2,
            'height': 5,
            'width': 10,
            'term': term,
        }
        m = menu.Menu(**kwargs)

        # Run test.
        act = str(m)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_content_relative_width_and_align_h_center(self):
        """When converted to a string, a Menu object returns a string
        that will draw the entire menu. If left content padding is set,
        the options will be inset by the amount of padding.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}          '
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(4, 0)}          '
            f'{term.reverse}'
            f'{term.move(0, 2)} spam'
            f'{term.normal}'
            f'{term.move(1, 2)} eggs'
            f'{term.move(2, 2)}bacon'
        )

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
            ],
            'option_align_h': 'right',
            'content_align_h': 'center',
            'content_relative_width': 0.8,
            'height': 5,
            'width': 10,
            'term': term,
        }
        m = menu.Menu(**kwargs)

        # Run test.
        act = str(m)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_overflow(self):
        """When converted to a string, a Menu object returns a string
        that will draw the entire menu. If there are too many options
        to fit in the panel, there should be an overflow indicator on
        the bottom line of the panel's content.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}         '
            f'{term.move(1, 0)}         '
            f'{term.move(2, 0)}         '
            f'{term.move(3, 0)}         '
            f'{term.move(4, 0)}         '
            f'{term.move(4, 0)}         '
            f'{term.move(4, 3)}[▼]'
            f'{term.reverse}'
            f'{term.move(0, 0)}spam  '
            f'{term.normal}'
            f'{term.move(1, 0)}eggs  '
            f'{term.move(2, 0)}bacon '
            f'{term.move(3, 0)}ham   '
        )

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
                menu.Option('ham', 'h'),
                menu.Option('beans', 'n'),
                menu.Option('toast', 'o'),
                menu.Option('tomato', 't'),
            ],
            'height': 5,
            'width': 9,
            'term': term,
        }
        m = menu.Menu(**kwargs)

        # Run test.
        act = str(m)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_select_bg_and_fg(self):
        """When converted to a string, a Menu object returns a string
        that will draw the entire menu. If foreground and background
        colors are set for the selection, the selection should be those
        colors.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}       '
            f'{term.move(1, 0)}       '
            f'{term.move(2, 0)}       '
            f'{term.move(3, 0)}       '
            f'{term.move(4, 0)}       '
            f'{term.red_on_blue}'
            f'{term.move(0, 0)}spam '
            f'{term.normal}'
            f'{term.move(1, 0)}eggs '
            f'{term.move(2, 0)}bacon'
        )

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
            ],
            'select_bg': 'blue',
            'select_fg': 'red',
            'height': 5,
            'width': 7,
            'term': term,
        }
        m = menu.Menu(**kwargs)

        # Run test.
        act = str(m)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_down_arrow(self):
        """When a down arrow is received, Menu.action() selects the
        next option.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(0, 0)}spam  '
            f'{term.reverse}'
            f'{term.move(1, 0)}eggs  '
            f'{term.normal}'
            f'{term.move(2, 0)}bacon '
            f'{term.move(3, 0)}ham   '
        ))

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
                menu.Option('ham', 'h'),
                menu.Option('beans', 'n'),
                menu.Option('toast', 'o'),
                menu.Option('tomato', 't'),
            ],
            'height': 5,
            'width': 9,
            'term': term,
        }
        m = menu.Menu(**kwargs)
        m._overflow_bottom = True
        m._stop = 4
        key = KEY_DOWN

        # Run test.
        act = m.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_down_arrow_at_bottom(self):
        """When a down arrow is received, Menu.action() selects the
        next option. If the selected option is the last option, the
        selection doesn't move.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(1, 0)}ham   '
            f'{term.move(2, 0)}beans '
            f'{term.move(3, 0)}toast '
            f'{term.reverse}'
            f'{term.move(4, 0)}tomato'
            f'{term.normal}'
        ))

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
                menu.Option('ham', 'h'),
                menu.Option('beans', 'n'),
                menu.Option('toast', 'o'),
                menu.Option('tomato', 't'),
            ],
            'height': 5,
            'width': 9,
            'term': term,
        }
        m = menu.Menu(**kwargs)
        m._overflow_top = True
        m._selected = 6
        m._start = 3
        m._stop = 7
        key = KEY_DOWN

        # Run test.
        act = m.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_down_arrow_scrolls_to_overflow(self):
        """When a down arrow is received, Menu.action() selects the
        next option. If the selected option is the last visible
        options and the list of option overflows, the list of options
        should scroll down to see the next option.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(0, 0)}         '
            f'{term.move(0, 3)}[▲]'
            f'{term.move(1, 0)}bacon '
            f'{term.move(2, 0)}ham   '
            f'{term.reverse}'
            f'{term.move(3, 0)}beans '
            f'{term.normal}'
        ))

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
                menu.Option('ham', 'h'),
                menu.Option('beans', 'n'),
                menu.Option('toast', 'o'),
                menu.Option('tomato', 't'),
            ],
            'height': 5,
            'width': 9,
            'term': term,
        }
        m = menu.Menu(**kwargs)
        m._overflow_bottom = True
        m._selected = 3
        m._stop = 4
        key = KEY_DOWN

        # Run test.
        act = m.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_down_arrow_scrolls_near_bottom_of_overflow(self):
        """When a down arrow is received, Menu.action() selects the
        next option. If the selected option is the last visible
        options and the list of option overflows, the list of options
        should scroll down to see the next option. If it scrolls to
        the next to last option, the overflow down marker should be
        replaced with the last option.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(4, 0)}         '
            f'{term.move(1, 0)}ham   '
            f'{term.move(2, 0)}beans '
            f'{term.reverse}'
            f'{term.move(3, 0)}toast '
            f'{term.normal}'
            f'{term.move(4, 0)}tomato'
        ))

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
                menu.Option('ham', 'h'),
                menu.Option('beans', 'n'),
                menu.Option('toast', 'o'),
                menu.Option('tomato', 't'),
            ],
            'height': 5,
            'width': 9,
            'term': term,
        }
        m = menu.Menu(**kwargs)
        m._overflow_bottom = True
        m._overflow_top = True
        m._selected = 4
        m._start = 2
        m._stop = 5
        key = KEY_DOWN

        # Run test.
        act = m.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_down_arrow_with_content_pad_left(self):
        """When a down arrow is received, Menu.action() selects the
        next option.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(0, 3)}spam  '
            f'{term.reverse}'
            f'{term.move(1, 3)}eggs  '
            f'{term.normal}'
            f'{term.move(2, 3)}bacon '
            f'{term.move(3, 3)}ham   '
        ))

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
                menu.Option('ham', 'h'),
                menu.Option('beans', 'n'),
                menu.Option('toast', 'o'),
                menu.Option('tomato', 't'),
            ],
            'content_pad_left': 0.2,
            'height': 5,
            'width': 10,
            'term': term,
        }
        m = menu.Menu(**kwargs)
        m._overflow_bottom = True
        m._stop = 4
        key = KEY_DOWN

        # Run test.
        act = m.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_end(self):
        """When an end is received, Menu.action() selects the
        last option and jumps to that section of the menu.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(4, 0)}         '
            f'{term.move(0, 0)}         '
            f'{term.move(0, 3)}[▲]'
            f'{term.move(1, 0)}ham   '
            f'{term.move(2, 0)}beans '
            f'{term.move(3, 0)}toast '
            f'{term.reverse}'
            f'{term.move(4, 0)}tomato'
            f'{term.normal}'
        ))

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
                menu.Option('ham', 'h'),
                menu.Option('beans', 'n'),
                menu.Option('toast', 'o'),
                menu.Option('tomato', 't'),
            ],
            'height': 5,
            'width': 9,
            'term': term,
        }
        m = menu.Menu(**kwargs)
        m._overflow_bottom = True
        m._selected = 2
        m._stop = 4
        key = KEY_END

        # Run test.
        act = m.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_home(self):
        """When a home is received, Menu.action() selects the
        first option and jumps to that section of the menu.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(4, 0)}         '
            f'{term.move(4, 3)}[▼]'
            f'{term.move(0, 0)}         '
            f'{term.reverse}'
            f'{term.move(0, 0)}spam  '
            f'{term.normal}'
            f'{term.move(1, 0)}eggs  '
            f'{term.move(2, 0)}bacon '
            f'{term.move(3, 0)}ham   '
        ))

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
                menu.Option('ham', 'h'),
                menu.Option('beans', 'n'),
                menu.Option('toast', 'o'),
                menu.Option('tomato', 't'),
            ],
            'height': 5,
            'width': 9,
            'term': term,
        }
        m = menu.Menu(**kwargs)
        m._overflow_top = True
        m._selected = 5
        m._start = 3
        m._stop = 7
        key = KEY_HOME

        # Run test.
        act = m.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_hotkey(self):
        """When a hotkey for an option is received, the selection
        jumps to that option.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(4, 0)}         '
            f'{term.move(4, 3)}[▼]'
            f'{term.move(0, 0)}         '
            f'{term.move(0, 0)}spam  '
            f'{term.reverse}'
            f'{term.move(1, 0)}eggs  '
            f'{term.normal}'
            f'{term.move(2, 0)}bacon '
            f'{term.move(3, 0)}ham   '
        ))

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
                menu.Option('ham', 'h'),
                menu.Option('beans', 'n'),
                menu.Option('toast', 'o'),
                menu.Option('tomato', 't'),
            ],
            'height': 5,
            'width': 9,
            'term': term,
        }
        m = menu.Menu(**kwargs)
        m._overflow_top = True
        m._selected = 5
        m._start = 3
        m._stop = 7
        key = KEY_E

        # Run test.
        act = m.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_hotkey_near_bottom_of_overflow(self):
        """When a hotkey for an option is received, the selection
        jumps to that option. If it jumps to the next to last option,
        that option should not be hidden by the overflow indicator.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(4, 0)}         '
            f'{term.move(0, 0)}         '
            f'{term.move(0, 3)}[▲]'
            f'{term.move(1, 0)}ham   '
            f'{term.move(2, 0)}beans '
            f'{term.reverse}'
            f'{term.move(3, 0)}toast '
            f'{term.normal}'
            f'{term.move(4, 0)}tomato'
        ))

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
                menu.Option('ham', 'h'),
                menu.Option('beans', 'n'),
                menu.Option('toast', 'o'),
                menu.Option('tomato', 't'),
            ],
            'height': 5,
            'width': 9,
            'term': term,
        }
        m = menu.Menu(**kwargs)
        m._overflow_top = False
        m._overflow_bottom = True
        m._selected = 0
        m._start = 0
        m._stop = 4
        key = KEY_O

        # Run test.
        act = m.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_page_down(self):
        """When a page down is received and the menu overflows,
        Menu.action() scrolls down by the height of the display and
        selects the option that is now in the position that was
        selected before the page down.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(1, 0)}toast '
            f'{term.reverse}'
            f'{term.move(2, 0)}tomato'
            f'{term.normal}'
            f'{term.move(3, 0)}coffee'
        ))

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
                menu.Option('ham', 'h'),
                menu.Option('beans', 'n'),
                menu.Option('toast', 'o'),
                menu.Option('tomato', 't'),
                menu.Option('coffee', 'c'),
                menu.Option('muffin', 'f'),
                menu.Option('grits ', 'g'),
            ],
            'height': 5,
            'width': 9,
            'term': term,
        }
        m = menu.Menu(**kwargs)
        m._overflow_top = True
        m._overflow_bottom = True
        m._selected = 3
        m._start = 2
        m._stop = 5
        key = KEY_PGDOWN

        # Run test.
        act = m.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_page_down_at_bottom(self):
        """When a page down is received and the selection would be
        greater than the number of options in the menu, the selection
        becomes the bottom option.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(1, 0)}tomato'
            f'{term.move(2, 0)}coffee'
            f'{term.move(3, 0)}muffin'
            f'{term.reverse}'
            f'{term.move(4, 0)}grits '
            f'{term.normal}'
        ))

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
                menu.Option('ham', 'h'),
                menu.Option('beans', 'n'),
                menu.Option('toast', 'o'),
                menu.Option('tomato', 't'),
                menu.Option('coffee', 'c'),
                menu.Option('muffin', 'f'),
                menu.Option('grits ', 'g'),
            ],
            'height': 5,
            'width': 9,
            'term': term,
        }
        m = menu.Menu(**kwargs)
        m._overflow_top = True
        m._overflow_bottom = False
        m._selected = 8
        m._start = 6
        m._stop = 10
        key = KEY_PGDOWN

        # Run test.
        act = m.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_page_down_from_top(self):
        """When a page down is received and the menu overflows,
        Menu.action() scrolls down by the height of the display and
        selects the option that is now in the position that was
        selected before the page down. If that position would now be
        covered by an top overflow indicator, scroll the menu up one
        line to keep the selected option visible.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(0, 0)}         '
            f'{term.move(0, 3)}[▲]'
            f'{term.reverse}'
            f'{term.move(1, 0)}beans '
            f'{term.normal}'
            f'{term.move(2, 0)}toast '
            f'{term.move(3, 0)}tomato'
        ))

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
                menu.Option('ham', 'h'),
                menu.Option('beans', 'n'),
                menu.Option('toast', 'o'),
                menu.Option('tomato', 't'),
                menu.Option('coffee', 'c'),
                menu.Option('muffin', 'f'),
                menu.Option('grits ', 'g'),
            ],
            'height': 5,
            'width': 9,
            'term': term,
        }
        m = menu.Menu(**kwargs)
        m._overflow_top = False
        m._overflow_bottom = True
        m._selected = 0
        m._start = 0
        m._stop = 4
        key = KEY_PGDOWN

        # Run test.
        act = m.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_page_up(self):
        """When a page up is received and the menu overflows,
        Menu.action() scrolls up by the height of the display and
        selects the option that is now in the position that was
        selected before the page up.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(1, 0)}bacon '
            f'{term.reverse}'
            f'{term.move(2, 0)}ham   '
            f'{term.normal}'
            f'{term.move(3, 0)}beans '
        ))

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
                menu.Option('ham', 'h'),
                menu.Option('beans', 'n'),
                menu.Option('toast', 'o'),
                menu.Option('tomato', 't'),
                menu.Option('coffee', 'c'),
                menu.Option('muffin', 'f'),
                menu.Option('grits ', 'g'),
            ],
            'height': 5,
            'width': 9,
            'term': term,
        }
        m = menu.Menu(**kwargs)
        m._overflow_top = True
        m._overflow_bottom = True
        m._selected = 6
        m._start = 5
        m._stop = 8
        key = KEY_PGUP

        # Run test.
        act = m.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_page_up_at_top(self):
        """When a page up is received and the selection would be
        less than zero, the selection becomes the top option.
        """
        # Expected values.
        exp = ('', (
            f'{term.reverse}'
            f'{term.move(0, 0)}spam  '
            f'{term.normal}'
            f'{term.move(1, 0)}eggs  '
            f'{term.move(2, 0)}bacon '
            f'{term.move(3, 0)}ham   '
        ))

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
                menu.Option('ham', 'h'),
                menu.Option('beans', 'n'),
                menu.Option('toast', 'o'),
                menu.Option('tomato', 't'),
                menu.Option('coffee', 'c'),
                menu.Option('muffin', 'f'),
                menu.Option('grits ', 'g'),
            ],
            'height': 5,
            'width': 9,
            'term': term,
        }
        m = menu.Menu(**kwargs)
        m._overflow_top = False
        m._overflow_bottom = True
        m._selected = 1
        m._start = 0
        m._stop = 4
        key = KEY_PGUP

        # Run test.
        act = m.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_page_up_from_bottom(self):
        """When a page up is received and the menu overflows,
        Menu.action() scrolls up by the height of the display and
        selects the option that is now in the position that was
        selected before the page up. If that position would now be
        covered by an top overflow indicator, scroll the menu down
        one line to keep the selected option visible.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(4, 0)}         '
            f'{term.move(4, 3)}[▼]'
            f'{term.move(1, 0)}ham   '
            f'{term.move(2, 0)}beans '
            f'{term.reverse}'
            f'{term.move(3, 0)}toast '
            f'{term.normal}'
        ))

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
                menu.Option('ham', 'h'),
                menu.Option('beans', 'n'),
                menu.Option('toast', 'o'),
                menu.Option('tomato', 't'),
                menu.Option('coffee', 'c'),
                menu.Option('muffin', 'f'),
                menu.Option('grits ', 'g'),
            ],
            'height': 5,
            'width': 9,
            'term': term,
        }
        m = menu.Menu(**kwargs)
        m._overflow_top = True
        m._overflow_bottom = False
        m._selected = 9
        m._start = 6
        m._stop = 10
        key = KEY_PGUP

        # Run test.
        act = m.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_enter(self):
        """When an enter is received, Menu.action() should return
        the name of the currently selected option as data.
        """
        # Expected values.
        exp = ('bacon', '')

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
                menu.Option('ham', 'h'),
                menu.Option('beans', 'n'),
                menu.Option('toast', 'o'),
                menu.Option('tomato', 't'),
            ],
            'height': 5,
            'width': 9,
            'term': term,
        }
        m = menu.Menu(**kwargs)
        m._overflow_bottom = True
        m._selected = 2
        m._stop = 4
        key = KEY_ENTER

        # Run test.
        act = m.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_unknown_key(self):
        """When an unknown key is received, its string value is returned
        as data.
        """
        # Expected values.
        exp = ('x', '')

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
                menu.Option('ham', 'h'),
                menu.Option('beans', 'n'),
                menu.Option('toast', 'o'),
                menu.Option('tomato', 't'),
            ],
            'height': 5,
            'width': 10,
            'term': Terminal(),
        }
        m = menu.Menu(**kwargs)
        m._overflow_bottom = True
        m._overflow_top = False
        m._start = 0
        m._stop = 4
        key = KEY_X

        # Run test.
        act = m.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_up_arrow(self):
        """When an up arrow is received, Menu.action() selects the
        previous option.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(0, 0)}spam  '
            f'{term.reverse}'
            f'{term.move(1, 0)}eggs  '
            f'{term.normal}'
            f'{term.move(2, 0)}bacon '
            f'{term.move(3, 0)}ham   '
        ))

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
                menu.Option('ham', 'h'),
                menu.Option('beans', 'n'),
                menu.Option('toast', 'o'),
                menu.Option('tomato', 't'),
            ],
            'height': 5,
            'width': 9,
            'term': term,
        }
        m = menu.Menu(**kwargs)
        m._overflow_bottom = True
        m._selected = 2
        m._stop = 4
        key = KEY_UP

        # Run test.
        act = m.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_up_arrow_at_bottom(self):
        """When an up arrow is received, Menu.action() selects the
        previous option. If this was done at the botom of the menu
        and the next option is visible, the menu does not scroll up.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(1, 0)}ham   '
            f'{term.move(2, 0)}beans '
            f'{term.reverse}'
            f'{term.move(3, 0)}toast '
            f'{term.normal}'
            f'{term.move(4, 0)}tomato'
        ))

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
                menu.Option('ham', 'h'),
                menu.Option('beans', 'n'),
                menu.Option('toast', 'o'),
                menu.Option('tomato', 't'),
            ],
            'height': 5,
            'width': 9,
            'term': term,
        }
        m = menu.Menu(**kwargs)
        m._overflow_bottom = False
        m._overflow_top = True
        m._selected = 6
        m._start = 3
        m._stop = 7
        key = KEY_UP

        # Run test.
        act = m.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_up_arrow_at_top(self):
        """When an up arrow is received, Menu.action() selects the
        previous option. If the selected option is the top option,
        the selection shouldn't move.
        """
        # Expected values.
        exp = ('', (
            f'{term.reverse}'
            f'{term.move(0, 0)}spam  '
            f'{term.normal}'
            f'{term.move(1, 0)}eggs  '
            f'{term.move(2, 0)}bacon '
            f'{term.move(3, 0)}ham   '
        ))

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
                menu.Option('ham', 'h'),
                menu.Option('beans', 'n'),
                menu.Option('toast', 'o'),
                menu.Option('tomato', 't'),
            ],
            'height': 5,
            'width': 9,
            'term': term,
        }
        m = menu.Menu(**kwargs)
        m._overflow_bottom = True
        m._selected = 0
        m._stop = 4
        key = KEY_UP

        # Run test.
        act = m.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_up_arrow_scrolls_to_overflow(self):
        """When an up arrow is received, Menu.action() selects the
        previous option. If the selected option is the first visible
        options and the list of option overflows, the list of options
        should scroll up to see the previous option.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(4, 0)}         '
            f'{term.move(4, 3)}[▼]'
            f'{term.reverse}'
            f'{term.move(1, 0)}bacon '
            f'{term.normal}'
            f'{term.move(2, 0)}ham   '
            f'{term.move(3, 0)}beans '
        ))

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
                menu.Option('ham', 'h'),
                menu.Option('beans', 'n'),
                menu.Option('toast', 'o'),
                menu.Option('tomato', 't'),
            ],
            'height': 5,
            'width': 9,
            'term': term,
        }
        m = menu.Menu(**kwargs)
        m._overflow_top = True
        m._selected = 3
        m._start = 3
        m._stop = 7
        key = KEY_UP

        # Run test.
        act = m.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_up_arrow_scrolls_near_top_of_overflow(self):
        """When a up arrow is received, Menu.action() selects the
        next option. If the selected option is the first visible
        options and the list of option overflows, the list of options
        should scroll up to see the next option. If it scrolls to
        the next to first option, the overflow up marker should be
        replaced with the first option.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(0, 0)}         '
            f'{term.move(0, 0)}spam  '
            f'{term.reverse}'
            f'{term.move(1, 0)}eggs  '
            f'{term.normal}'
            f'{term.move(2, 0)}bacon '
            f'{term.move(3, 0)}ham   '
        ))

        # Test data and state.
        kwargs = {
            'options': [
                menu.Option('spam', 's'),
                menu.Option('eggs', 'e'),
                menu.Option('bacon', 'b'),
                menu.Option('ham', 'h'),
                menu.Option('beans', 'n'),
                menu.Option('toast', 'o'),
                menu.Option('tomato', 't'),
            ],
            'height': 5,
            'width': 9,
            'term': term,
        }
        m = menu.Menu(**kwargs)
        m._overflow_bottom = True
        m._overflow_top = True
        m._selected = 2
        m._start = 2
        m._stop = 5
        key = KEY_UP

        # Run test.
        act = m.action(key)

        # Determine test result.
        self.assertEqual(exp, act)
