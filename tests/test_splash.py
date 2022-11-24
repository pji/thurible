"""
test_splash
~~~~~~~~~~~

Unit tests for the `thurible.splash` module.
"""
import unittest as ut

from blessed import Terminal
from blessed.keyboard import Keystroke

from thurible import splash as s
import tests.test_panel as tp


# Common values.
term = tp.term


# Test case.
class SplashTestCase(tp.TerminalTestCase):
    def test___init__optional_parameters(self):
        """Given any parameters, a TitlePanel should return an
        object with the expected attributes set.
        """
        # Expected values.
        exp = {
            'content': 'bacon',
            **tp.kwargs_content_opt_set,
            **tp.kwargs_title_opt_set,
            **tp.kwargs_frame_opt_set,
            **tp.kwargs_panel_req,
            **tp.kwargs_panel_opt_set,
        }

        # Run test.
        panel = s.Splash(**exp)

        # Gather actuals.
        act = {key: getattr(panel, key) for key in exp}

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
            **tp.kwargs_content_opt_default,
            **tp.kwargs_title_opt_default,
            **tp.kwargs_frame_opt_default,
            **tp.kwargs_panel_opt_default
        }

        # Run test.
        panel = s.Splash(**exp_req)

        # Gather actuals.
        act_req = {key: getattr(panel, key) for key in exp_req}
        act_opt = {key: getattr(panel, key) for key in exp_opt}

        # Determine test results.
        self.assertDictEqual(exp_req, act_req)
        self.assertDictEqual(exp_opt, act_opt)

    def test___str__(self):
        """When converted to a string, a TitlePanel object returns a
        string that will draw the entire splash screen.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(1, 2)}┌┐'
            f'{term.move(2, 2)}└┐'
            f'{term.move(3, 2)}└┘'
        )

        # Test data and state.
        kwargs = {
            'content': (
                '┌┐\n'
                '└┐\n'
                '└┘'
            ),
            'height': 5,
            'width': 6,
            'term': term,
        }
        panel = s.Splash(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_content_align_h_left(self):
        """When converted to a string, a TitlePanel object returns
        a string that will draw the entire splash screen. If the
        horizontal content align is set to left, the text of the
        content should be left aligned within the panel.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(1, 0)}┌┐'
            f'{term.move(2, 0)}└┐'
            f'{term.move(3, 0)}└┘'
        )

        # Test data and state.
        kwargs = {
            'content': (
                '┌┐\n'
                '└┐\n'
                '└┘'
            ),
            'content_align_h': 'left',
            'height': 5,
            'width': 6,
            'term': term,
        }
        panel = s.Splash(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_content_align_h_right(self):
        """When converted to a string, a TitlePanel object returns
        a string that will draw the entire splash screen. If the
        horizontal content align is set to right, the text of the
        content should be right aligned within the panel.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(1, 4)}┌┐'
            f'{term.move(2, 4)}└┐'
            f'{term.move(3, 4)}└┘'
        )

        # Test data and state.
        kwargs = {
            'content': (
                '┌┐\n'
                '└┐\n'
                '└┘'
            ),
            'content_align_h': 'right',
            'height': 5,
            'width': 6,
            'term': term,
        }
        panel = s.Splash(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_content_align_v_bottom(self):
        """When converted to a string, a TitlePanel object returns
        a string that will draw the entire splash screen. If the
        vertical content align is set to bottom, the text of the
        content should be bottom aligned within the panel.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(2, 2)}┌┐'
            f'{term.move(3, 2)}└┐'
            f'{term.move(4, 2)}└┘'
        )

        # Test data and state.
        kwargs = {
            'content': (
                '┌┐\n'
                '└┐\n'
                '└┘'
            ),
            'content_align_v': 'bottom',
            'height': 5,
            'width': 6,
            'term': term,
        }
        panel = s.Splash(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_content_align_v_top(self):
        """When converted to a string, a TitlePanel object returns
        a string that will draw the entire splash screen. If the
        vertical content align is set to top, the text of the
        content should be top aligned within the panel.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(0, 2)}┌┐'
            f'{term.move(1, 2)}└┐'
            f'{term.move(2, 2)}└┘'
        )

        # Test data and state.
        kwargs = {
            'content': (
                '┌┐\n'
                '└┐\n'
                '└┘'
            ),
            'content_align_v': 'top',
            'height': 5,
            'width': 6,
            'term': term,
        }
        panel = s.Splash(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)
