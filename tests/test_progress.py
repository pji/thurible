"""
test_progress
~~~~~~~~~~~~~

Unit tests for the :mod:`thurible.progress` module.
"""
from collections import deque
from datetime import timedelta

import pytest as pt

from thurible import progress


# Test case.
def test__init_default(
    content_attr_defaults,
    frame_attr_defaults,
    panel_attr_defaults,
    title_attr_defaults
):
    """Given only the required parameters, a
    :class:`progress.Progress` panel Should return an object
    with the expected attributes set.
    """
    panel = progress.Progress(steps=6)
    assert panel.steps == 6
    assert panel.progress == 0
    assert panel.bar_bg == ''
    assert panel.bar_fg == ''
    assert panel.max_messages == 0
    assert panel.messages == deque(maxlen=0)
    assert not panel.timestamp
    assert {
        k: getattr(panel, k) for k in content_attr_defaults
    } == content_attr_defaults
    assert {
        k: getattr(panel, k) for k in title_attr_defaults
    } == title_attr_defaults
    assert {
        k: getattr(panel, k) for k in frame_attr_defaults
    } == frame_attr_defaults
    assert {
        k: getattr(panel, k) for k in panel_attr_defaults
    } == panel_attr_defaults


def test__init_set(
    content_attr_set,
    frame_attr_set,
    panel_attr_set,
    title_attr_set
):
    """Given any parameters, a :class:`progress.Progress` panel
    should return an object with the expected attributes set.
    """
    panel = progress.Progress(
        steps=6,
        progress=2,
        bar_bg='red',
        bar_fg='blue',
        max_messages=5,
        messages=deque([], maxlen=5),
        timestamp=True,
        **content_attr_set,
        **title_attr_set,
        **frame_attr_set,
        **panel_attr_set
    )
    assert panel.steps == 6
    assert panel.progress == 2
    assert panel.bar_bg == 'red'
    assert panel.bar_fg == 'blue'
    assert panel.max_messages == 5
    assert panel.messages == deque([], maxlen=5)
    assert panel.timestamp
    assert {
        k: getattr(panel, k) for k in content_attr_set
    } == content_attr_set
    assert {
        k: getattr(panel, k) for k in title_attr_set
    } == title_attr_set
    assert {
        k: getattr(panel, k) for k in frame_attr_set
    } == frame_attr_set
    assert {
        k: getattr(panel, k) for k in panel_attr_set
    } == panel_attr_set


def test_as_str(term):
    """When converted to a string, a :class:`progress.Progress`
    panel returns a string that will draw the entire progress bar.
    """
    panel = progress.Progress(
        steps=6,
        height=5,
        width=6
    )
    assert str(panel) == (
        f'{term.move(0, 0)}      '
        f'{term.move(1, 0)}      '
        f'{term.move(2, 0)}      '
        f'{term.move(3, 0)}      '
        f'{term.move(4, 0)}      '
        f'{term.move(2, 0)}      '
    )


def test_as_str_with_bar_bg(term):
    """When converted to a string, a :class:`progress.Progress`
    panel returns a string that will draw the entire progress bar.
    If a background color is assigned to the bar, the unfilled
    portion of that bar should be that color.
    """
    panel = progress.Progress(
        steps=6,
        height=5,
        width=6,
        bar_bg='red'
    )
    assert str(panel) == (
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


def test_as_str_with_bar_bg_and_bar_fg(term):
    """When converted to a string, a :class:`progress.Progress`
    panel returns a string that will draw the entire progress bar.
    If a background color is assigned to the bar, the unfilled
    portion of that bar should be that color.
    """
    panel = progress.Progress(
        steps=6,
        height=5,
        width=6,
        bar_bg='red',
        bar_fg='blue'
    )
    assert str(panel) == (
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


def test_as_str_with_bar_fg(term):
    """When converted to a string, a :class:`progress.Progress`
    panel returns a string that will draw the entire progress bar.
    If a foreground color is assigned to the bar, the filled
    portion of that bar should be that color.
    """
    panel = progress.Progress(
        steps=6,
        height=5,
        width=6,
        bar_fg='red'
    )
    assert str(panel) == (
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


def test_as_str_with_bar_bg_and_progress(term):
    """When converted to a string, a :class:`progress.Progress`
    panel returns a string that will draw the entire progress bar.
    If a background color is assigned to the bar, the unfilled
    portion of that bar should be that color. If any progress has
    been made, the progress bar is advanced that many steps.
    """
    panel = progress.Progress(
        steps=6,
        height=5,
        width=6,
        bar_bg='red',
        progress=4
    )
    assert str(panel) == (
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


def test_as_str_with_max_messages(term):
    """When converted to a string, a :class:`progress.Progress`
    panel returns a string that will draw the entire progress bar.
    If :attr:`Progress.max_messages` is set, space is created for
    that number of messages.
    """
    panel = progress.Progress(
        steps=6,
        height=5,
        width=6,
        max_messages=2
    )
    assert str(panel) == (
        f'{term.move(0, 0)}      '
        f'{term.move(1, 0)}      '
        f'{term.move(2, 0)}      '
        f'{term.move(3, 0)}      '
        f'{term.move(4, 0)}      '
        f'{term.move(1, 0)}      '
    )


def test_as_str_with_max_messages_and_messages(term):
    """When converted to a string, a :class:`progress.Progress`
    panel returns a string that will draw the entire progress bar.
    If :attr:`Progress.max_messages` is set, space is created for
    that number of messages. If :attr:`Progress.messages` is set,
    those messages appear in the display.
    """
    panel = progress.Progress(
        steps=6,
        height=5,
        width=6,
        max_messages=2,
        messages=['spam', 'eggs',]
    )
    assert str(panel) == (
        f'{term.move(0, 0)}      '
        f'{term.move(1, 0)}      '
        f'{term.move(2, 0)}      '
        f'{term.move(3, 0)}      '
        f'{term.move(4, 0)}      '
        f'{term.move(1, 0)}      '
        f'{term.move(2, 0)}eggs  '
        f'{term.move(3, 0)}spam  '
    )


def test_as_str_with_progress(term):
    """When converted to a string, a :class:`progress.Progress`
    panel returns a string that will draw the entire progress bar.
    If any progress has been made, the progress bar is advanced
    that many steps.
    """
    panel = progress.Progress(
        steps=6,
        height=5,
        width=6,
        progress=4
    )
    assert str(panel) == (
        f'{term.move(0, 0)}      '
        f'{term.move(1, 0)}      '
        f'{term.move(2, 0)}      '
        f'{term.move(3, 0)}      '
        f'{term.move(4, 0)}      '
        f'{term.move(2, 0)}████  '
    )


def test_as_str_with_progress_and_content_pad(term):
    """When converted to a string, a :class:`progress.Progress`
    panel returns a string that will draw the entire progress bar.
    If any progress has been made, the progress bar is advanced
    that many steps.
    """
    panel = progress.Progress(
        steps=6,
        height=5,
        width=10,
        progress=4,
        content_pad_left=0.2,
        content_pad_right=0.2
    )
    assert str(panel) == (
        f'{term.move(0, 0)}          '
        f'{term.move(1, 0)}          '
        f'{term.move(2, 0)}          '
        f'{term.move(3, 0)}          '
        f'{term.move(4, 0)}          '
        f'{term.move(2, 2)}████  '
    )


def test_as_str_with_progress_and_content_relative_width(term):
    """When converted to a string, a :class:`progress.Progress`
    panel returns a string that will draw the entire progress bar.
    If any progress has been made, the progress bar is advanced
    that many steps. If a relative width is given, the bar's width
    is that percentage of the panel's width.
    """
    panel = progress.Progress(
        steps=6,
        height=5,
        width=10,
        progress=4,
        content_relative_width=0.6
    )
    assert str(panel) == (
        f'{term.move(0, 0)}          '
        f'{term.move(1, 0)}          '
        f'{term.move(2, 0)}          '
        f'{term.move(3, 0)}          '
        f'{term.move(4, 0)}          '
        f'{term.move(2, 2)}████  '
    )


def test_as_str_with_steps_greater_than_width_and_progress(term):
    """When converted to a string, a :class:`progress.Progress`
    panel returns a string that will draw the entire progress bar.
    If any progress has been made, the progress bar is advanced
    that many steps. If there are more steps than there are
    columns in the panel's width, each character can be split
    into eighths.
    """
    panel = progress.Progress(
        steps=6 * 8,
        height=5,
        width=6,
        progress=3 * 8 + 5
    )
    assert str(panel) == (
        f'{term.move(0, 0)}      '
        f'{term.move(1, 0)}      '
        f'{term.move(2, 0)}      '
        f'{term.move(3, 0)}      '
        f'{term.move(4, 0)}      '
        f'{term.move(2, 0)}███▋  '
    )


def test_as_str_with_steps_greater_than_width_and_progress_full(term):
    """When converted to a string, a :class:`progress.Progress`
    panel returns a string that will draw the entire progress bar.
    If any progress has been made, the progress bar is advanced
    that many steps. If all the steps are complete, the bar should
    be full.
    """
    panel = progress.Progress(
        steps=6 * 8,
        height=5,
        width=6,
        progress=6 * 8
    )
    assert str(panel) == (
        f'{term.move(0, 0)}      '
        f'{term.move(1, 0)}      '
        f'{term.move(2, 0)}      '
        f'{term.move(3, 0)}      '
        f'{term.move(4, 0)}      '
        f'{term.move(2, 0)}██████'
    )


def test_as_str_with_steps_not_mult_of_eight_and_progress_full(term):
    """When converted to a string, a :class:`progress.Progress`
    panel returns a string that will draw the entire progress bar.
    If any progress has been made, the progress bar is advanced
    that many steps. If all the steps are complete, the bar should
    be full. This should even be true when the number of steps is
    not divisible by eight.
    """
    panel = progress.Progress(
        steps=6 * 8 - 3,
        height=5,
        width=6,
        progress=6 * 8 - 3
    )
    assert str(panel) == (
        f'{term.move(0, 0)}      '
        f'{term.move(1, 0)}      '
        f'{term.move(2, 0)}      '
        f'{term.move(3, 0)}      '
        f'{term.move(4, 0)}      '
        f'{term.move(2, 0)}██████'
    )


def test_update_notick_with_timestamp(term, mocker):
    """When passed a NoTick message, Progress.update() should
    return a string that will not advance the progress bar. If
    not in notick mode, the message should be added to the top
    of the status messages. If :attr:`Progress.timestamp` is
    `True`, add a timestamp to the beginning of the messages.
    """
    mock_dt = mocker.patch('thurible.progress.datetime')
    mock_dt.now.return_value = timedelta(seconds=3)
    panel = progress.Progress(
        steps=6,
        height=5,
        width=18,
        progress=4,
        timestamp=True,
        max_messages=2,
        messages=['spam', 'eggs',]
    )
    msg = progress.NoTick('bacon')
    mock_dt.now.return_value = timedelta(seconds=5)
    assert panel.update(msg) == (
        f'{term.move(1, 0)}████████████      '
        f'{term.move(2, 0)}00:02 bacon       '
        f'{term.move(3, 0)}00:00 eggs        '
    )


def test_update_notick_after_notick_with_timestamp(term, mocker):
    """When passed a NoTick message, Progress.update() should
    return a string that will not advance the progress bar. If
    not in notick mode, the message should be added to the top
    of the status messages. If :attr:`Progress.timestamp` is
    `True`, add a timestamp to the beginning of the messages.
    """
    mock_dt = mocker.patch('thurible.progress.datetime')
    mock_dt.now.return_value = timedelta(seconds=3)
    panel = progress.Progress(
        steps=6,
        height=5,
        width=18,
        progress=4,
        timestamp=True,
        max_messages=2,
        messages=['spam', 'eggs',]
    )
    msg = progress.NoTick('bacon')
    panel.update(msg)
    mock_dt.now.return_value = timedelta(seconds=5)
    msg = progress.NoTick('ham')
    mock_dt.now.return_value = timedelta(seconds=7)
    assert panel.update(msg) == (
        f'{term.move(1, 0)}████████████      '
        f'{term.move(2, 0)}00:04 ham         '
        f'{term.move(3, 0)}00:00 eggs        '
    )


def test_update_tick(term):
    """When passed a Tick message, Progress.update() should
    return a string that will advance the progress bar.
    """
    panel = progress.Progress(
        steps=6,
        height=5,
        width=6,
        progress=3,
        timestamp=True
    )
    msg = progress.Tick()
    assert panel.update(msg) == f'{term.move(2, 0)}████  '


def test_update_tick_with_message(term):
    """When passed a Tick message, Progress.update() should
    return a string that will advance the progress bar.
    """
    panel = progress.Progress(
        steps=6,
        height=5,
        width=6,
        progress=3,
        max_messages=2,
        messages=['spam', 'eggs',],
    )
    msg = progress.Tick('bacon')
    assert panel.update(msg) == (
        f'{term.move(1, 0)}████  '
        f'{term.move(2, 0)}bacon '
        f'{term.move(3, 0)}eggs  '
    )


def test_update_tick_after_notick_with_message_and_timestamp(term, mocker):
    """When passed a Tick message, Progress.update() should
    return a string that will advance the progress bar. If
    :attr:`Progress.timestamp` is `True`, add a timestamp to
    the beginning of the messages. If this is sent after a
    :class:`thurible.progress.NoTick` message has been sent,
    this message should replace the top message.
    """
    mock_dt = mocker.patch('thurible.progress.datetime')
    mock_dt.now.return_value = timedelta(seconds=3)
    panel = progress.Progress(
        steps=6,
        height=5,
        width=18,
        progress=3,
        timestamp=True,
        max_messages=2,
        messages=['spam', 'eggs',]
    )
    msg = progress.NoTick('bacon')
    mock_dt.now.return_value = timedelta(seconds=5)
    panel.update(msg)
    msg = progress.Tick('ham')
    mock_dt.now.return_value = timedelta(seconds=7)
    assert panel.update(msg) == (
        f'{term.move(1, 0)}████████████      '
        f'{term.move(2, 0)}00:04 ham         '
        f'{term.move(3, 0)}00:00 eggs        '
    )


def test_update_tick_with_message_and_timestamp(term, mocker):
    """When passed a Tick message, Progress.update() should
    return a string that will advance the progress bar. If
    :attr:`Progress.timestamp` is `True`, add a timestamp to
    the beginning of the messages.
    """
    mock_dt = mocker.patch('thurible.progress.datetime')
    mock_dt.now.return_value = timedelta(seconds=3)
    panel = progress.Progress(
        steps=6,
        height=5,
        width=18,
        progress=3,
        timestamp=True,
        max_messages=2,
        messages=['spam', 'eggs',]
    )
    msg = progress.Tick('bacon')
    mock_dt.now.return_value = timedelta(seconds=5)
    assert panel.update(msg) == (
        f'{term.move(1, 0)}████████████      '
        f'{term.move(2, 0)}00:02 bacon       '
        f'{term.move(3, 0)}00:00 eggs        '
    )
