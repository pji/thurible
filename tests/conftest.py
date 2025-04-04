"""
conftest
~~~~~~~~

Common fixtures for :mod:`thurible` tests.
"""
from pathlib import Path
from queue import Queue

import pytest as pt
from blessed.keyboard import Keystroke

from thurible import menu
from thurible.util import get_terminal


# Hooks.
def pytest_assertrepr_compare(config, op, left, right):
    """Hooks into assertions to neutralize terminal escapes. This
    keeps the cursor from jumping around when printing output
    from failed test.
    """
    def sanitize_str(s):
        if isinstance(s, str) and '\x1b' in s:
            parts = s.split('\x1b')
            for i in range(len(parts) - 1):
                parts[i + 1] = '\u241b' + parts[i + 1]
            parts = [f' {part!r}' for part in parts]
            return parts
        return s

    def sanitize_seq(seq):
        sanitized = [
            sanitize_str(item)
            for item in seq
        ]
        if seq != sanitized:
            result = []
            for new, old in zip(sanitized, seq):
                if isinstance(old, str) and not isinstance(new, str):
                    result.extend(new)
                    result[-1] = result[-1] + ','
                else:
                    result.append(f'  {new!r},')
            if isinstance(seq, tuple):
                result = ['(', *result, ')',]
            else:
                result = ['[', *result, ']',]
            return result
        return eq

    def sanitize(item):
        if isinstance(item, (tuple, list)):
            return sanitize_seq(item)
        if isinstance(item, str):
            return sanitize_str(item)
        return item

    newleft = sanitize(left)
    newright = sanitize(right)
    if newleft != left or newright != right:
        if not isinstance(newleft, list):
            newleft = [newleft,]
        if not isinstance(newright, list):
            newright = [newright,]
        opp_ops = {
            '==': '!=',
            '!=': '==',
            'is': 'is not',
            'is not': 'is',
        }
        opp_ops.setdefault(op, '???')
        return [
            'Comparing results:',
            '   vals:',
            *newleft,
            '',
            opp_ops[op],
            '',
            *newright
        ]
    return None


# Fixtures.
@pt.fixture
def term():
    """A terminal object."""
    return get_terminal()


# Common key strokes.
@pt.fixture
def KEY_BACKSPACE(term):
    """The backspace key."""
    return Keystroke('\x08', term.KEY_BACKSPACE, 'KEY_BACKSPACE')


@pt.fixture
def KEY_BELL(term):
    """The backspace key."""
    return Keystroke('\x07', term.KEY_BELL, 'KEY_BELL')


@pt.fixture
def KEY_DELETE(term):
    """The delete key."""
    return Keystroke('\x1b[3~]', term.KEY_DELETE, 'KEY_DELETE')


@pt.fixture
def KEY_DOWN(term):
    """The down arrow key."""
    return Keystroke('\x1b[B', term.KEY_DOWN, 'KEY_DOWN')


@pt.fixture
def KEY_E(term):
    """The end key."""
    return Keystroke('e')


@pt.fixture
def KEY_END(term):
    """The end key."""
    return Keystroke('\x1b[F', term.KEY_END, 'KEY_END')


@pt.fixture
def KEY_ENTER(term):
    """The enter key."""
    return Keystroke('\n', term.KEY_ENTER, 'KEY_ENTER')


@pt.fixture
def KEY_F1(term):
    """The F1 key."""
    return Keystroke('\x1bOP', term.KEY_F1, 'KEY_F1')


@pt.fixture
def KEY_HOME(term):
    """The home key."""
    return Keystroke('\x1b[H', term.KEY_HOME, 'KEY_HOME')


@pt.fixture
def KEY_LEFT(term):
    """The left arrow key."""
    return Keystroke('\x1b[D', term.KEY_LEFT, 'KEY_LEFT')


@pt.fixture
def KEY_O(term):
    """The o key."""
    return Keystroke('o')


@pt.fixture
def KEY_PGDOWN(term):
    """The page down key."""
    return Keystroke('\x1b[U', term.KEY_PGDOWN, 'KEY_PGDOWN')


@pt.fixture
def KEY_PGUP(term):
    """The page up key."""
    return Keystroke('\x1b[V', term.KEY_PGUP, 'KEY_PGUP')


@pt.fixture
def KEY_RIGHT(term):
    """The right arrow key."""
    return Keystroke('\x1b[C', term.KEY_RIGHT, 'KEY_RIGHT')


@pt.fixture
def KEY_S(term):
    """The end key."""
    return Keystroke('s')


@pt.fixture
def KEY_UP(term):
    """The left arrow key."""
    return Keystroke('\x1b[A', term.KEY_UP, 'KEY_UP')


@pt.fixture
def KEY_X(term):
    """The x key."""
    return Keystroke('x')


@pt.fixture
def KEY_Y(term):
    """The y key."""
    return Keystroke('y')


# Default values for class/protocol attributes.
@pt.fixture
def content_attr_defaults():
    """Default values for `Content` attributes."""
    return {
        'content_align_h': 'center',
        'content_align_v': 'middle',
        'content_relative_width': 1.0,
    }


@pt.fixture
def content_attr_defaults_menu():
    """Default for the Menu values for `Content` attributes."""
    return {
        'content_align_h': 'left',
        'content_align_v': 'top',
        'content_relative_width': 1.0,
    }


@pt.fixture
def frame_attr_defaults():
    """Default values for `Frame` attributes."""
    return {
        'frame_type': None,
        'frame_bg': '',
        'frame_fg': '',
    }


@pt.fixture
def panel_attr_defaults(term):
    """Default values for `Panel` attributes."""
    return {
        'height': term.height,
        'width': term.width,
        'term': term,
        'origin_y': 0,
        'origin_x': 0,
        'bg': '',
        'fg': '',
        'panel_pad_bottom': 0.0,
        'panel_pad_left': 0.0,
        'panel_pad_right': 0.0,
        'panel_pad_top': 0.0,
        'panel_relative_height': 1.0,
        'panel_relative_width': 1.0,
        'panel_align_h': 'center',
        'panel_align_v': 'middle',
    }


@pt.fixture
def title_attr_defaults():
    """Default values for `Title` attributes."""
    return {
        'footer_text': '',
        'footer_align': 'left',
        'footer_frame': False,
        'title_text': '',
        'title_align': 'left',
        'title_frame': False,
        'title_bg': '',
        'title_fg': '',
    }


# Standard values for setting class/protocol attributes.
@pt.fixture
def content_attr_set():
    """Set values for `Content` attributes."""
    return {
        'content_align_h': 'right',
        'content_align_v': 'bottom',
        'content_relative_width': 0.6,
    }


@pt.fixture
def frame_attr_set():
    """Set values for `Frame` attributes."""
    return {
        'frame_type': 'light',
        'frame_bg': 'red',
        'frame_fg': 'blue',
    }


@pt.fixture
def panel_attr_set():
    """Set values for `Panel` attributes."""
    return {
        'height': 5,
        'width': 7,
        'term': term,
        'origin_y': 2,
        'origin_x': 3,
        'fg': 'red',
        'bg': 'blue',
        'panel_pad_bottom': 0.3,
        'panel_pad_left': 0.1,
        'panel_pad_right': 0.2,
        'panel_pad_top': 0.4,
        'panel_relative_height': 0.3,
        'panel_relative_width': 0.7,
    }


@pt.fixture
def title_attr_set():
    """Set values for `Title` attributes."""
    return {
        'footer_text': 'eggs',
        'footer_align': 'center',
        'footer_frame': True,
        'title_text': 'spam',
        'title_align': 'center',
        'title_frame': True,
        'title_bg': 'blue',
        'title_fg': 'red',
    }


# File locations and directory contents.
@pt.fixture
def test_data_contents():
    dir = Path('tests/data')
    return [path for path in dir.iterdir()]


# Mocking to simplify testing.
@pt.fixture
def mock_thread(mocker):
    mocked = mocker.patch('threading.Thread')
    yield mocked


@pt.fixture
def queues(mocker):
    queues = (Queue(), Queue())
    mocker.patch('thurible.util.get_queues', return_value=queues)
    yield queues


# Menu options.
@pt.fixture
def menu_options():
    """Very long list of common menu options."""
    return [
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
    ]
