"""
test_progress
~~~~~~~~~~~~~

Unit tests for the :mod:`thurible.progress` module.
"""
import unittest as ut

from tests import test_panel as tp
from thurible import progress
from thurible.util import get_terminal


# Common data.
term = get_terminal()


# Test case.
class ProgressTestCase(tp.TerminalTestCase):
    def test___init__optional_parameters(self):
        """Given any parameters, a :class:`progress.Progress` panel
        should return an object with the expected attributes set.
        """
        # Expected values.
        exp = {
            'steps': 6,
            'progress': 2,
            'bar_bg': 'red',
            'bar_fg': 'blue',
            **tp.kwargs_content_opt_set,
            **tp.kwargs_title_opt_set,
            **tp.kwargs_frame_opt_set,
            **tp.kwargs_panel_req,
            **tp.kwargs_panel_opt_set,
        }

        # Run test.
        panel = progress.Progress(**exp)

        # Gather actuals.
        act = {key: getattr(panel, key) for key in exp}

        # Determine test results.
        self.assertDictEqual(exp, act)

    def test___init__required_parameters(self):
        """Given only the required parameters, a
        :class:`progress.Progress` panel Should return an object
        with the expected attributes set.
        """
        # Expected values.
        exp_req = {
            'steps': 6,
            **tp.kwargs_panel_req
        }
        exp_opt = {
            'progress': 0,
            'bar_bg': '',
            'bar_fg': '',
            **tp.kwargs_content_opt_default,
            **tp.kwargs_title_opt_default,
            **tp.kwargs_frame_opt_default,
            **tp.kwargs_panel_opt_default
        }

        # Run test.
        panel = progress.Progress(**exp_req)

        # Gather actuals.
        act_req = {key: getattr(panel, key) for key in exp_req}
        act_opt = {key: getattr(panel, key) for key in exp_opt}

        # Determine test results.
        self.assertDictEqual(exp_req, act_req)
        self.assertDictEqual(exp_opt, act_opt)

    def test___str__(self):
        """When converted to a string, a :class:`progress.Progress`
        panel returns a string that will draw the entire progress bar.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(2, 0)}      '
        )

        # Test data and state.
        kwargs = {
            'steps': 6,
            'height': 5,
            'width': 6,
        }
        panel = progress.Progress(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_bar_bg(self):
        """When converted to a string, a :class:`progress.Progress`
        panel returns a string that will draw the entire progress bar.
        If a background color is assigned to the bar, the unfilled
        portion of that bar should be that color.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(2, 0)}'
            f'{term.on_red}'
            '      '
            f'{term.normal}'
        )

        # Test data and state.
        kwargs = {
            'steps': 6,
            'bar_bg': 'red',
            'height': 5,
            'width': 6,
        }
        panel = progress.Progress(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_bar_bg_and_bar_fg(self):
        """When converted to a string, a :class:`progress.Progress`
        panel returns a string that will draw the entire progress bar.
        If a background color is assigned to the bar, the unfilled
        portion of that bar should be that color.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(2, 0)}'
            f'{term.blue_on_red}'
            '      '
            f'{term.normal}'
        )

        # Test data and state.
        kwargs = {
            'steps': 6,
            'bar_bg': 'red',
            'bar_fg': 'blue',
            'height': 5,
            'width': 6,
        }
        panel = progress.Progress(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_bar_fg(self):
        """When converted to a string, a :class:`progress.Progress`
        panel returns a string that will draw the entire progress bar.
        If a foreground color is assigned to the bar, the filled
        portion of that bar should be that color.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(2, 0)}'
            f'{term.red}'
            '      '
            f'{term.normal}'
        )

        # Test data and state.
        kwargs = {
            'steps': 6,
            'bar_fg': 'red',
            'height': 5,
            'width': 6,
        }
        panel = progress.Progress(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_bar_bg_and_progress(self):
        """When converted to a string, a :class:`progress.Progress`
        panel returns a string that will draw the entire progress bar.
        If a background color is assigned to the bar, the unfilled
        portion of that bar should be that color. If any progress has
        been made, the progress bar is advanced that many steps.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(2, 0)}'
            f'{term.on_red}'
            '████  '
            f'{term.normal}'
        )

        # Test data and state.
        kwargs = {
            'steps': 6,
            'progress': 4,
            'bar_bg': 'red',
            'height': 5,
            'width': 6,
        }
        panel = progress.Progress(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_progress(self):
        """When converted to a string, a :class:`progress.Progress`
        panel returns a string that will draw the entire progress bar.
        If any progress has been made, the progress bar is advanced
        that many steps.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(2, 0)}████  '
        )

        # Test data and state.
        kwargs = {
            'steps': 6,
            'progress': 4,
            'height': 5,
            'width': 6,
        }
        panel = progress.Progress(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_steps_greater_than_width_and_progress(self):
        """When converted to a string, a :class:`progress.Progress`
        panel returns a string that will draw the entire progress bar.
        If any progress has been made, the progress bar is advanced
        that many steps. If there are more steps than there are
        columns in the panel's width, each character can be split
        into eighths.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(2, 0)}███▋  '
        )

        # Test data and state.
        kwargs = {
            'steps': 6 * 8,
            'progress': 3 * 8 + 5,
            'height': 5,
            'width': 6,
        }
        panel = progress.Progress(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_steps_greater_than_width_and_progress_full(self):
        """When converted to a string, a :class:`progress.Progress`
        panel returns a string that will draw the entire progress bar.
        If any progress has been made, the progress bar is advanced
        that many steps. If all the steps are complete, the bar should
        be full.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(2, 0)}██████'
        )

        # Test data and state.
        kwargs = {
            'steps': 6 * 8,
            'progress': 6 * 8,
            'height': 5,
            'width': 6,
        }
        panel = progress.Progress(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_steps_not_mult_of_eight_and_progress_full(self):
        """When converted to a string, a :class:`progress.Progress`
        panel returns a string that will draw the entire progress bar.
        If any progress has been made, the progress bar is advanced
        that many steps. If all the steps are complete, the bar should
        be full. This should even be true when the number of steps is
        not divisible by eight.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(2, 0)}██████'
        )

        # Test data and state.
        kwargs = {
            'steps': 6 * 8 - 3,
            'progress': 6 * 8 - 3,
            'height': 5,
            'width': 6,
        }
        panel = progress.Progress(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_update(self):
        """When passed a Tick message, Progress.update() should
        return a string that will advance the progress bar.
        """
        # Expected value.
        exp = term.move(2, 0) + '████  '

        # Test data and state.
        kwargs = {
            'steps': 6,
            'progress': 3,
            'height': 5,
            'width': 6,
        }
        panel = progress.Progress(**kwargs)
        msg = progress.Tick()

        # Run test.
        act = panel.update(msg)

        # Determine test result.
        self.assertEqual(exp, act)
