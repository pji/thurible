"""
test_log
~~~~~~~~

Unit tests for the `thurible.log` module.
"""
from collections import deque

from tests import test_panel as tp
from thurible import log
from thurible.util import get_terminal


# Common data.
term = get_terminal()


# Test case.
class LogTestCase(tp.TerminalTestCase):
    def test___init__optional_parameters(self):
        """Given any parameters, a `log.Log` panel should return an
        object with the expected attributes set.
        """
        # Expected values.
        exp = {
            'content': deque(['spam', 'eggs', 'bacon',]),
            'maxlen': 100,
            **tp.kwargs_content_opt_set,
            **tp.kwargs_title_opt_set,
            **tp.kwargs_frame_opt_set,
            **tp.kwargs_panel_req,
            **tp.kwargs_panel_opt_set,
        }

        # Run test.
        panel = log.Log(**exp)

        # Gather actuals.
        act = {key: getattr(panel, key) for key in exp}

        # Determine test results.
        self.assertDictEqual(exp, act)

    def test___init__required_parameters(self):
        """Given only the required parameters, a `log.Log` panel should
        return an object with the expected attributes set.
        """
        # Expected values.
        exp_req = tp.kwargs_panel_req
        exp_opt = {
            'content': deque(),
            'maxlen': 50,
            **tp.kwargs_content_opt_default,
            **tp.kwargs_title_opt_default,
            **tp.kwargs_frame_opt_default,
            **tp.kwargs_panel_opt_default
        }

        # Run test.
        panel = log.Log(**exp_req)

        # Gather actuals.
        act_req = {key: getattr(panel, key) for key in exp_req}
        act_opt = {key: getattr(panel, key) for key in exp_opt}

        # Determine test results.
        self.assertDictEqual(exp_req, act_req)
        self.assertDictEqual(exp_opt, act_opt)

    def test___str__(self):
        """When converted to a string, a `log.Log` panel returns a
        string that will draw the entire splash screen.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(0, 0)}eggs'
            f'{term.move(1, 0)}spam'
        )

        # Test data and state.
        kwargs = {
            'content': ('spam', 'eggs',),
            'height': 5,
            'width': 6,
        }
        panel = log.Log(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__content_overflows_height(self):
        """When converted to a string, a `log.Log` panel returns a
        string that will draw the entire splash screen. If there are
        more lines of content than can fit in the panel, the panel
        only displays the top portion of the content that fits in the
        panel.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(0, 0)}toast'
            f'{term.move(1, 0)}beans'
            f'{term.move(2, 0)}ham'
            f'{term.move(3, 0)}bacon'
            f'{term.move(4, 0)}eggs'
        )

        # Test data and state.
        kwargs = {
            'content': ('spam', 'eggs', 'bacon', 'ham', 'beans', 'toast'),
            'height': 5,
            'width': 6,
        }
        panel = log.Log(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__content_overflows_maxlen(self):
        """When converted to a string, a `log.Log` panel returns a
        string that will draw the entire splash screen. If there are
        more lines of content than the maximum length of the log, the
        log should drop the overflowing lines.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(0, 0)}toast'
            f'{term.move(1, 0)}beans'
            f'{term.move(2, 0)}ham'
        )

        # Test data and state.
        kwargs = {
            'content': ('spam', 'eggs', 'bacon', 'ham', 'beans', 'toast'),
            'maxlen': 3,
            'height': 5,
            'width': 6,
        }
        panel = log.Log(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__content_overflows_width(self):
        """When converted to a string, a `log.Log` panel returns a
        string that will draw the entire splash screen. If any of
        the lines of content are too long for the panel, they are
        wrapped to the next line.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(0, 0)}bacon'
            f'{term.move(1, 0)}ham'
            f'{term.move(2, 0)}spam'
            f'{term.move(3, 0)}eggs'
        )

        # Test data and state.
        kwargs = {
            'content': ('spam eggs', 'bacon ham'),
            'height': 5,
            'width': 6,
        }
        panel = log.Log(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_update(self):
        """Given an Update message with a string, Log.update() should
        add that string to the top of the log display.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(0, 0)}bacon'
            f'{term.move(1, 0)}eggs'
            f'{term.move(2, 0)}spam'
        )

        # Test data and state.
        kwargs = {
            'content': ('spam', 'eggs',),
            'height': 5,
            'width': 6,
        }
        panel = log.Log(**kwargs)
        msg = log.Update('bacon')

        # Run test.
        act = panel.update(msg)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_update_overflow_maxlen(self):
        """Given an Update message with a string, Log.update() should
        add that string to the top of the log display. If the number of
        lines becomes longer than the maximum length of the log, the
        overflowing lines should be dropped.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(0, 0)}bacon'
            f'{term.move(1, 0)}eggs'
        )

        # Test data and state.
        kwargs = {
            'content': ('spam', 'eggs',),
            'maxlen': 2,
            'height': 5,
            'width': 6,
        }
        panel = log.Log(**kwargs)
        msg = log.Update('bacon')

        # Run test.
        act = panel.update(msg)

        # Determine test result.
        self.assertEqual(exp, act)
