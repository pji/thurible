"""
test_progress
~~~~~~~~~~~~~

Unit tests for the :mod:`thurible.progress` module.
"""
from collections import deque
from datetime import timedelta
import unittest as ut
from unittest.mock import patch

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
            'max_messages': 5,
            'messages': deque([], maxlen=5),
            'timestamp': True,
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
            'max_messages': 0,
            'messages': deque(maxlen=0),
            'timestamp': False,
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

    def test___str__with_max_messages(self):
        """When converted to a string, a :class:`progress.Progress`
        panel returns a string that will draw the entire progress bar.
        If :attr:`Progress.max_messages` is set, space is created for
        that number of messages.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(1, 0)}      '
        )

        # Test data and state.
        kwargs = {
            'steps': 6,
            'max_messages': 2,
            'height': 5,
            'width': 6,
        }
        panel = progress.Progress(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_max_messages_and_messages(self):
        """When converted to a string, a :class:`progress.Progress`
        panel returns a string that will draw the entire progress bar.
        If :attr:`Progress.max_messages` is set, space is created for
        that number of messages. If :attr:`Progress.messages` is set,
        those messages appear in the display.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}eggs  '
            f'{term.move(3, 0)}spam  '
        )

        # Test data and state.
        kwargs = {
            'steps': 6,
            'max_messages': 2,
            'messages': ['spam', 'eggs',],
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

    def test___str__with_progress_and_content_pad(self):
        """When converted to a string, a :class:`progress.Progress`
        panel returns a string that will draw the entire progress bar.
        If any progress has been made, the progress bar is advanced
        that many steps.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}          '
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(4, 0)}          '
            f'{term.move(2, 2)}████  '
        )

        # Test data and state.
        kwargs = {
            'steps': 6,
            'progress': 4,
            'height': 5,
            'width': 10,
            'content_pad_left': 0.2,
            'content_pad_right': 0.2,
        }
        panel = progress.Progress(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_progress_and_content_relative_width(self):
        """When converted to a string, a :class:`progress.Progress`
        panel returns a string that will draw the entire progress bar.
        If any progress has been made, the progress bar is advanced
        that many steps. If a relative width is given, the bar's width
        is that percentage of the panel's width.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}          '
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(4, 0)}          '
            f'{term.move(2, 2)}████  '
        )

        # Test data and state.
        kwargs = {
            'steps': 6,
            'progress': 4,
            'height': 5,
            'width': 10,
            'content_relative_width': 0.6,
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

    @patch('thurible.progress.datetime')
    def test_update_notick_with_timestamp(self, mock_dt):
        """When passed a NoTick message, Progress.update() should
        return a string that will not advance the progress bar. If
        not in notick mode, the message should be added to the top
        of the status messages. If :attr:`Progress.timestamp` is
        `True`, add a timestamp to the beginning of the messages.
        """
        # Expected value.
        exp = (
            f'{term.move(1, 0)}████████████      '
            f'{term.move(2, 0)}00:02 bacon       '
            f'{term.move(3, 0)}00:00 eggs        '
        )

        # Test data and state.
        kwargs = {
            'steps': 6,
            'progress': 4,
            'max_messages': 2,
            'timestamp': True,
            'messages': ['spam', 'eggs',],
            'height': 5,
            'width': 18,
        }
        mock_dt.now.return_value = timedelta(seconds=3)
        panel = progress.Progress(**kwargs)
        msg = progress.NoTick('bacon')
        mock_dt.now.return_value = timedelta(seconds=5)

        # Run test.
        act = panel.update(msg)

        # Determine test result.
        self.assertEqual(exp, act)

    @patch('thurible.progress.datetime')
    def test_update_notick_after_notick_with_timestamp(self, mock_dt):
        """When passed a NoTick message, Progress.update() should
        return a string that will not advance the progress bar. If
        not in notick mode, the message should be added to the top
        of the status messages. If :attr:`Progress.timestamp` is
        `True`, add a timestamp to the beginning of the messages.
        """
        # Expected value.
        exp = (
            f'{term.move(1, 0)}████████████      '
            f'{term.move(2, 0)}00:04 ham         '
            f'{term.move(3, 0)}00:00 eggs        '
        )

        # Test data and state.
        kwargs = {
            'steps': 6,
            'progress': 4,
            'max_messages': 2,
            'timestamp': True,
            'messages': ['spam', 'eggs',],
            'height': 5,
            'width': 18,
        }
        mock_dt.now.return_value = timedelta(seconds=3)
        panel = progress.Progress(**kwargs)
        msg = progress.NoTick('bacon')
        mock_dt.now.return_value = timedelta(seconds=5)
        act = panel.update(msg)
        msg = progress.NoTick('ham')
        mock_dt.now.return_value = timedelta(seconds=7)

        # Run test.
        act = panel.update(msg)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_update_tick(self):
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

    def test_update_tick_with_message(self):
        """When passed a Tick message, Progress.update() should
        return a string that will advance the progress bar.
        """
        # Expected value.
        exp = (
            f'{term.move(1, 0)}████  '
            f'{term.move(2, 0)}bacon '
            f'{term.move(3, 0)}eggs  '
        )

        # Test data and state.
        kwargs = {
            'steps': 6,
            'progress': 3,
            'max_messages': 2,
            'messages': ['spam', 'eggs',],
            'height': 5,
            'width': 6,
        }
        panel = progress.Progress(**kwargs)
        msg = progress.Tick('bacon')

        # Run test.
        act = panel.update(msg)

        # Determine test result.
        self.assertEqual(exp, act)

    @patch('thurible.progress.datetime')
    def test_update_tick_after_notick_with_message_and_timestamp(
        self,
        mock_dt
    ):
        """When passed a Tick message, Progress.update() should
        return a string that will advance the progress bar. If
        :attr:`Progress.timestamp` is `True`, add a timestamp to
        the beginning of the messages. If this is sent after a
        :class:`thurible.progress.NoTick` message has been sent,
        this message should replace the top message.
        """
        # Expected value.
        exp = (
            f'{term.move(1, 0)}████████████      '
            f'{term.move(2, 0)}00:04 ham         '
            f'{term.move(3, 0)}00:00 eggs        '
        )

        # Test data and state.
        kwargs = {
            'steps': 6,
            'progress': 3,
            'max_messages': 2,
            'timestamp': True,
            'messages': ['spam', 'eggs',],
            'height': 5,
            'width': 18,
        }
        mock_dt.now.return_value = timedelta(seconds=3)
        panel = progress.Progress(**kwargs)
        msg = progress.NoTick('bacon')
        mock_dt.now.return_value = timedelta(seconds=5)
        act = panel.update(msg)
        msg = progress.Tick('ham')
        mock_dt.now.return_value = timedelta(seconds=7)

        # Run test.
        act = panel.update(msg)

        # Determine test result.
        self.assertEqual(exp, act)

    @patch('thurible.progress.datetime')
    def test_update_tick_with_message_and_timestamp(self, mock_dt):
        """When passed a Tick message, Progress.update() should
        return a string that will advance the progress bar. If
        :attr:`Progress.timestamp` is `True`, add a timestamp to
        the beginning of the messages.
        """
        # Expected value.
        exp = (
            f'{term.move(1, 0)}████████████      '
            f'{term.move(2, 0)}00:02 bacon       '
            f'{term.move(3, 0)}00:00 eggs        '
        )

        # Test data and state.
        kwargs = {
            'steps': 6,
            'progress': 3,
            'max_messages': 2,
            'timestamp': True,
            'messages': ['spam', 'eggs',],
            'height': 5,
            'width': 18,
        }
        mock_dt.now.return_value = timedelta(seconds=3)
        panel = progress.Progress(**kwargs)
        msg = progress.Tick('bacon')
        mock_dt.now.return_value = timedelta(seconds=5)

        # Run test.
        act = panel.update(msg)

        # Determine test result.
        self.assertEqual(exp, act)
