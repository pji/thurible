"""
test_text
~~~~~~~~~

Unit tests for the termui.text module.
"""
import unittest as ut

from blessed import Terminal
from blessed.keyboard import Keystroke

from thurible import text
import tests.test_panel as tp


# Common data.
term = tp.term
KEY_DOWN = Keystroke('\x1b[B', term.KEY_DOWN, 'KEY_DOWN')
KEY_END = Keystroke('\x1b[F', term.KEY_END, 'KEY_END')
KEY_HOME = Keystroke('\x1b[H', term.KEY_HOME, 'KEY_HOME')
KEY_PGDOWN = Keystroke('\x1b[U', term.KEY_PGDOWN, 'KEY_PGDOWN')
KEY_PGUP = Keystroke('\x1b[V', term.KEY_PGUP, 'KEY_PGUP')
KEY_UP = Keystroke('\x1b[A', term.KEY_UP, 'KEY_UP')
KEY_X = Keystroke('x')


# Test case.
class TextTestCase(tp.TerminalTestCase):
    def test___init__optional_parameters(self):
        """Given any parameters, a TitlePanel should return an
        object with the expected attributes set.
        """
        # Expected values.
        exp = {
            'content': 'bacon',
            **tp.kwargs_content_opt_default_alt,
            **tp.kwargs_title_opt_set,
            **tp.kwargs_frame_opt_set,
            **tp.kwargs_panel_req,
            **tp.kwargs_panel_opt_set,
        }

        # Run test.
        t = text.Text(**exp)

        # Gather actuals.
        act = {key: getattr(t, key) for key in exp}

        # Determine test results.
        self.assertDictEqual(exp, act)

    def test___init__required_parameters(self):
        """Given only the required parameters, a TitlePanel should
        return an object with the expected attributes set.
        """
        # Expected values.
        exp_req = tp.kwargs_panel_req

        exp_opt = {
            'content': '',
            **tp.kwargs_content_opt_default_alt,
            **tp.kwargs_title_opt_default,
            **tp.kwargs_frame_opt_default,
            **tp.kwargs_panel_opt_default,
        }

        # Run test.
        t = text.Text(**exp_req)

        # Gather actuals.
        act_req = {key: getattr(t, key) for key in exp_req}
        act_opt = {key: getattr(t, key) for key in exp_opt}

        # Determine test results.
        self.assertDictEqual(exp_req, act_req)
        self.assertDictEqual(exp_opt, act_opt)

    def test___str__(self):
        """When converted to a string, a Text object returns a string
        that will draw the text.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}          '
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(4, 0)}          '
            f'{term.move(0, 0)}spam'
        )

        # Test data and state.
        kwargs = {
            'content': 'spam',
            'height': 5,
            'width': 10,
            'term': term,
        }
        t = text.Text(**kwargs)

        # Run test.
        act = str(t)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_bg_and_fg(self):
        """When converted to a string, a Text object returns a string
        that will draw the text. If foreground and background colors
        are set, the contents should be those colors.
        """
        # Expected values.
        exp = (
            f'{term.red_on_blue}'
            f'{term.move(0, 0)}          '
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(4, 0)}          '
            f'{term.normal}'
            f'{term.red_on_blue}'
            f'{term.move(0, 0)}spam'
            f'{term.normal}'
        )

        # Test data and state.
        kwargs = {
            'content': 'spam',
            'height': 5,
            'width': 10,
            'term': term,
            'bg': 'blue',
            'fg': 'red',
        }
        t = text.Text(**kwargs)

        # Run test.
        act = str(t)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_bottom_overflow(self):
        """When converted to a string, a Text object returns a string
        that will draw the text. If the text overflows the bottom of
        the display, there should be an indicator showing there is
        overflow.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}          '
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(4, 0)}          '
            f'{term.move(4, 0)}          '
            f'{term.move(4, 3)}[▼]'
            f'{term.move(0, 0)}spam eggs'
            f'{term.move(1, 0)}eggs spam'
            f'{term.move(2, 0)}spam eggs'
            f'{term.move(3, 0)}eggs spam'
        )

        # Test data and state.
        kwargs = {
            'content': (
                'spam eggs '
                'eggs spam '
                'spam eggs '
                'eggs spam '
                'spam eggs '
                'eggs spam '
            ),
            'height': 5,
            'width': 10,
            'term': Terminal(),
        }
        t = text.Text(**kwargs)

        # Run test.
        act = str(t)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_bottom_overflow_and_bg_and_fg(self):
        """When converted to a string, a Text object returns a string
        that will draw the text. If the text overflows the bottom of
        the display, there should be an indicator showing there is
        overflow. If there are foreground and background colors set,
        the overflow indicator and the contents should be those colors.
        """
        # Expected values.
        exp = (
            f'{term.red_on_blue}'
            f'{term.move(0, 0)}          '
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(4, 0)}          '
            f'{term.normal}'
            f'{term.red_on_blue}'
            f'{term.move(4, 0)}          '
            f'{term.move(4, 3)}[▼]'
            f'{term.normal}'
            f'{term.red_on_blue}'
            f'{term.move(0, 0)}spam eggs'
            f'{term.move(1, 0)}eggs spam'
            f'{term.move(2, 0)}spam eggs'
            f'{term.move(3, 0)}eggs spam'
            f'{term.normal}'
        )

        # Test data and state.
        kwargs = {
            'content': (
                'spam eggs '
                'eggs spam '
                'spam eggs '
                'eggs spam '
                'spam eggs '
                'eggs spam '
            ),
            'height': 5,
            'width': 10,
            'term': term,
            'bg': 'blue',
            'fg': 'red',
        }
        t = text.Text(**kwargs)

        # Run test.
        act = str(t)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_down_arrow(self):
        """When a down arrow is received, Text.action() scrolls down
        in the text.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(0, 0)}          '
            f'{term.move(0, 3)}[▲]'
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(1, 0)}2pam eggs'
            f'{term.move(2, 0)}3pam eggs'
            f'{term.move(3, 0)}4pam eggs'
        ))

        # Test data and state.
        kwargs = {
            'content': (
                '0pam eggs '
                '1pam eggs '
                '2pam eggs '
                '3pam eggs '
                '4pam eggs '
                '5pam eggs '
                '6pam eggs '
                '7pam eggs '
                '8pam eggs '
                '9pam eggs '
            ),
            'height': 5,
            'width': 10,
            'term': term,
        }
        t = text.Text(**kwargs)
        t._overflow_bottom = True
        t._stop = 4
        key = KEY_DOWN

        # Run test.
        act = t.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_down_arrow_cannot_scroll_past_end(self):
        """When a down arrow is received, Text.action() scrolls down
        in the text. If already at the bottom of the text, Text.action()
        cannot scroll any farther.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(4, 0)}          '
            f'{term.move(1, 0)}6pam eggs'
            f'{term.move(2, 0)}7pam eggs'
            f'{term.move(3, 0)}8pam eggs'
            f'{term.move(4, 0)}9pam eggs'
        ))

        # Test data and state.
        kwargs = {
            'content': (
                '0pam eggs '
                '1pam eggs '
                '2pam eggs '
                '3pam eggs '
                '4pam eggs '
                '5pam eggs '
                '6pam eggs '
                '7pam eggs '
                '8pam eggs '
                '9pam eggs '
            ),
            'height': 5,
            'width': 10,
            'term': term,
        }
        t = text.Text(**kwargs)
        t._overflow_bottom = False
        t._overflow_top = True
        t._start = 6
        t._stop = 10
        key = KEY_DOWN

        # Run test.
        act = t.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_down_arrow_text_smaller_than_screen(self):
        """When a down arrow is received, Text.action() scrolls down
        in the text. If the text is too small to scroll, no update is
        returned.
        """
        # Expected values.
        exp = ('', '')

        # Test data and state.
        kwargs = {
            'content': (
                '0pam eggs '
                '1pam eggs '
            ),
            'height': 5,
            'width': 10,
            'term': term,
        }
        t = text.Text(**kwargs)
        t._start = 0
        t._stop = 4
        key = KEY_DOWN

        # Run test.
        act = t.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_down_arrow_reach_near_bottom(self):
        """When a down arrow is received, Text.action() scrolls down
        in the text. If the bottom of the text is reached, the bottom
        overflow indicator should not be shown.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(4, 0)}          '
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(4, 0)}          '
            f'{term.move(1, 0)}6pam eggs'
            f'{term.move(2, 0)}7pam eggs'
            f'{term.move(3, 0)}8pam eggs'
            f'{term.move(4, 0)}9pam eggs'
        ))

        # Test data and state.
        kwargs = {
            'content': (
                '0pam eggs '
                '1pam eggs '
                '2pam eggs '
                '3pam eggs '
                '4pam eggs '
                '5pam eggs '
                '6pam eggs '
                '7pam eggs '
                '8pam eggs '
                '9pam eggs '
            ),
            'height': 5,
            'width': 10,
            'term': term,
        }
        t = text.Text(**kwargs)
        t._overflow_bottom = True
        t._overflow_top = True
        t._start = 5
        t._stop = 8
        key = KEY_DOWN

        # Run test.
        act = t.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_end(self):
        """When a end is received, Text.action() scrolls down
        to the end of the text.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(4, 0)}          '
            f'{term.move(0, 0)}          '
            f'{term.move(0, 3)}[▲]'
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(4, 0)}          '
            f'{term.move(1, 0)}6pam eggs'
            f'{term.move(2, 0)}7pam eggs'
            f'{term.move(3, 0)}8pam eggs'
            f'{term.move(4, 0)}9pam eggs'
        ))

        # Test data and state.
        kwargs = {
            'content': (
                '0pam eggs '
                '1pam eggs '
                '2pam eggs '
                '3pam eggs '
                '4pam eggs '
                '5pam eggs '
                '6pam eggs '
                '7pam eggs '
                '8pam eggs '
                '9pam eggs '
            ),
            'height': 5,
            'width': 10,
            'term': term,
        }
        t = text.Text(**kwargs)
        t._overflow_bottom = True
        t._stop = 4
        key = KEY_END

        # Run test.
        act = t.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_home(self):
        """When a home is received, Text.action() scrolls up
        to the top of the text.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(4, 0)}          '
            f'{term.move(4, 3)}[▼]'
            f'{term.move(0, 0)}          '
            f'{term.move(0, 0)}          '
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(0, 0)}0pam eggs'
            f'{term.move(1, 0)}1pam eggs'
            f'{term.move(2, 0)}2pam eggs'
            f'{term.move(3, 0)}3pam eggs'
        ))

        # Test data and state.
        kwargs = {
            'content': (
                '0pam eggs '
                '1pam eggs '
                '2pam eggs '
                '3pam eggs '
                '4pam eggs '
                '5pam eggs '
                '6pam eggs '
                '7pam eggs '
                '8pam eggs '
                '9pam eggs '
            ),
            'height': 5,
            'width': 10,
            'term': Terminal(),
        }
        t = text.Text(**kwargs)
        t._overflow_bottom = False
        t._overflow_top = True
        t._start = 6
        t._stop = 10
        key = KEY_HOME

        # Run test.
        act = t.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_page_down(self):
        """When a page down is received, Text.action() scrolls down
        a page in the text.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(0, 0)}          '
            f'{term.move(0, 3)}[▲]'
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(1, 0)}4pam eggs'
            f'{term.move(2, 0)}5pam eggs'
            f'{term.move(3, 0)}6pam eggs'
        ))

        # Test data and state.
        kwargs = {
            'content': (
                '0pam eggs '
                '1pam eggs '
                '2pam eggs '
                '3pam eggs '
                '4pam eggs '
                '5pam eggs '
                '6pam eggs '
                '7pam eggs '
                '8pam eggs '
                '9pam eggs '
            ),
            'height': 5,
            'width': 10,
            'term': term,
        }
        t = text.Text(**kwargs)
        t._overflow_bottom = True
        t._stop = 4
        key = KEY_PGDOWN

        # Run test.
        act = t.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_page_up(self):
        """When a page up is received, Text.action() scrolls up
        a page in the text.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(4, 0)}          '
            f'{term.move(4, 3)}[▼]'
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(1, 0)}3pam eggs'
            f'{term.move(2, 0)}4pam eggs'
            f'{term.move(3, 0)}5pam eggs'
        ))

        # Test data and state.
        kwargs = {
            'content': (
                '0pam eggs '
                '1pam eggs '
                '2pam eggs '
                '3pam eggs '
                '4pam eggs '
                '5pam eggs '
                '6pam eggs '
                '7pam eggs '
                '8pam eggs '
                '9pam eggs '
            ),
            'height': 5,
            'width': 10,
            'term': term,
        }
        t = text.Text(**kwargs)
        t._overflow_bottom = False
        t._overflow_top = True
        t._start = 6
        t._stop = 10
        key = KEY_PGUP

        # Run test.
        act = t.action(key)

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
            'content': (
                '0pam eggs '
                '1pam eggs '
                '2pam eggs '
                '3pam eggs '
                '4pam eggs '
                '5pam eggs '
                '6pam eggs '
                '7pam eggs '
                '8pam eggs '
                '9pam eggs '
            ),
            'height': 5,
            'width': 10,
            'term': Terminal(),
        }
        t = text.Text(**kwargs)
        t._overflow_bottom = True
        t._overflow_top = False
        t._start = 0
        t._stop = 4
        key = KEY_X

        # Run test.
        act = t.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_up_arrow(self):
        """When a up arrow is received, Text.action() scrolls up
        in the text.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(4, 0)}          '
            f'{term.move(4, 3)}[▼]'
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(1, 0)}5pam eggs'
            f'{term.move(2, 0)}6pam eggs'
            f'{term.move(3, 0)}7pam eggs'
        ))

        # Test data and state.
        kwargs = {
            'content': (
                '0pam eggs '
                '1pam eggs '
                '2pam eggs '
                '3pam eggs '
                '4pam eggs '
                '5pam eggs '
                '6pam eggs '
                '7pam eggs '
                '8pam eggs '
                '9pam eggs '
            ),
            'height': 5,
            'width': 10,
            'term': term,
        }
        t = text.Text(**kwargs)
        t._overflow_bottom = False
        t._overflow_top = True
        t._start = 6
        t._stop = 10
        key = KEY_UP

        # Run test.
        act = t.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_up_arrow_cannot_scroll_past_top(self):
        """When a up arrow is received, Text.action() scrolls up
        in the text. If already at the bottom of the text, Text.action()
        cannot scroll any farther.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(0, 0)}          '
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(0, 0)}0pam eggs'
            f'{term.move(1, 0)}1pam eggs'
            f'{term.move(2, 0)}2pam eggs'
            f'{term.move(3, 0)}3pam eggs'
        ))

        # Test data and state.
        kwargs = {
            'content': (
                '0pam eggs '
                '1pam eggs '
                '2pam eggs '
                '3pam eggs '
                '4pam eggs '
                '5pam eggs '
                '6pam eggs '
                '7pam eggs '
                '8pam eggs '
                '9pam eggs '
            ),
            'height': 5,
            'width': 10,
            'term': term,
        }
        t = text.Text(**kwargs)
        t._overflow_bottom = True
        t._overflow_top = False
        t._start = 0
        t._stop = 4
        key = KEY_UP

        # Run test.
        act = t.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_up_arrow_reach_near_top(self):
        """When a up arrow is received, Text.action() scrolls up
        in the text. If the top of the text is reaches, the top
        overflow indicator should not be shown.
        """
        # Expected values.
        exp = ('', (
            f'{term.move(0, 0)}          '
            f'{term.move(0, 0)}          '
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(0, 0)}0pam eggs'
            f'{term.move(1, 0)}1pam eggs'
            f'{term.move(2, 0)}2pam eggs'
            f'{term.move(3, 0)}3pam eggs'
        ))

        # Test data and state.
        kwargs = {
            'content': (
                '0pam eggs '
                '1pam eggs '
                '2pam eggs '
                '3pam eggs '
                '4pam eggs '
                '5pam eggs '
                '6pam eggs '
                '7pam eggs '
                '8pam eggs '
                '9pam eggs '
            ),
            'height': 5,
            'width': 10,
            'term': term,
        }
        t = text.Text(**kwargs)
        t._overflow_bottom = True
        t._overflow_top = True
        t._start = 2
        t._stop = 5
        key = KEY_UP

        # Run test.
        act = t.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action_up_arrow_text_smaller_than_screen(self):
        """When a up arrow is received, Text.action() scrolls up
        in the text. If the text is too small to scroll, no update is
        returned.
        """
        # Expected values.
        exp = ('', '')

        # Test data and state.
        kwargs = {
            'content': (
                '0pam eggs '
                '1pam eggs '
            ),
            'height': 5,
            'width': 10,
            'term': Terminal(),
        }
        t = text.Text(**kwargs)
        t._start = 0
        t._stop = 4
        key = KEY_UP

        # Run test.
        act = t.action(key)

        # Determine test result.
        self.assertEqual(exp, act)
