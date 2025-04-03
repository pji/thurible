"""
test_panel
~~~~~~~~~~

Unit tests for the `thurible.panel` module.
"""
from dataclasses import dataclass
import unittest as ut
from unittest.mock import call, patch, PropertyMock
from types import MethodType

import pytest as pt
from blessed import Terminal
from blessed.keyboard import Keystroke

from thurible import panel as p
from thurible.messages import Message
from thurible.util import get_terminal


# Common values.
term = get_terminal()
kwargs_content_opt_default = {
    'content_align_h': 'center',
    'content_align_v': 'middle',
    'content_relative_width': 1.0,
}
kwargs_content_opt_default_alt = kwargs_content_opt_default.copy()
kwargs_content_opt_default_alt['content_align_h'] = 'left'
kwargs_content_opt_default_alt['content_align_v'] = 'top'
kwargs_content_opt_set = {
    'content_align_h': 'right',
    'content_align_v': 'bottom',
    'content_relative_width': 0.6,
}
kwargs_frame_opt_default = {
    'frame_type': None,
    'frame_bg': '',
    'frame_fg': '',
}
kwargs_frame_opt_set = {
    'frame_type': 'light',
    'frame_bg': 'red',
    'frame_fg': 'blue',
}
kwargs_panel_opt_default = {
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
kwargs_panel_opt_set = {
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
kwargs_panel_req = {
}
kwargs_title_opt_default = {
    'footer_text': '',
    'footer_align': 'left',
    'footer_frame': False,
    'title_text': '',
    'title_align': 'left',
    'title_frame': False,
    'title_bg': '',
    'title_fg': '',
}
kwargs_title_opt_set = {
    'footer_text': 'eggs',
    'footer_align': 'center',
    'footer_frame': True,
    'title_text': 'spam',
    'title_align': 'center',
    'title_frame': True,
    'title_bg': 'blue',
    'title_fg': 'red',
}


# Parent class.
class TerminalTestCase(ut.TestCase):
    def assertEqual(self, a, b):
        if (
            isinstance(a, tuple)
            and isinstance(b, tuple)
            and len(a) == len(b)
            and all(isinstance(a_, str) for a_ in a)
            and all(isinstance(b_, str) for b_ in b)
        ):
            for a_, b_ in zip(a, b):
                self.assertEqual(a_, b_)
        elif (
            isinstance(a, list)
            and isinstance(b, list)
            and len(a) == len(b)
            and all(isinstance(a_, type(call)) for a_ in a)
            and all(isinstance(b_, type(call)) for b_ in b)
        ):
            for a_, b_ in zip(a, b):
                self.assertEqual(a_, b_)
        elif (
            isinstance(a, type(call))
            and isinstance(b, type(call))
        ):
            self.assertEqual(a[0], b[0])
            for a_, b_ in zip(a[1], b[1]):
                self.assertEqual(a_, b_)
            self.assertEqual(a[1], b[1])
        if isinstance(a, str) and '\x1b' in a:
            a = a.split('\x1b')
            if not a[0]:
                a = a[1:]
            a = [f'\x1b{s}' for s in a]
        if isinstance(b, str) and '\x1b' in b:
            b = b.split('\x1b')
            if not b[0]:
                b = b[1:]
            b = [f'\x1b{s}' for s in b]
        super().assertEqual(a, b)


# Test case.
class TestFrame:
    # Initiation tests.
    def test__init_attrs_default(
        self, frame_attr_defaults, panel_attr_defaults
    ):
        """Given only the required parameters, a Panel subclass should
        return an object with the expected attributes set.
        """
        panel = p.Frame()
        assert {
            k: getattr(panel, k) for k in frame_attr_defaults
        } == frame_attr_defaults
        assert {
            k: getattr(panel, k) for k in panel_attr_defaults
        } == panel_attr_defaults

    def test__init_attrs_set(
        self, frame_attr_set, panel_attr_set
    ):
        """Given only the required parameters, a Panel subclass should
        return an object with the expected attributes set.
        """
        panel = p.Frame(
            **frame_attr_set,
            **panel_attr_set
        )
        assert {
            k: getattr(panel, k) for k in frame_attr_set
        } == frame_attr_set
        assert {
            k: getattr(panel, k) for k in panel_attr_set
        } == panel_attr_set

    # String coercion tests.
    def test_as_str(self, capsys, term):
        """When converted to a string, a Pane object returns a string
        that will draw the entire splash screen.
        """
        panel = p.Frame(height=5, width=6, frame_type='light')
        assert str(panel) == (
            f'{term.move(1, 1)}    '
            f'{term.move(2, 1)}    '
            f'{term.move(3, 1)}    '
            f'{term.move(0, 0)}┌────┐'
            f'{term.move(1, 0)}│'
            f'{term.move(1, 5)}│'
            f'{term.move(2, 0)}│'
            f'{term.move(2, 5)}│'
            f'{term.move(3, 0)}│'
            f'{term.move(3, 5)}│'
            f'{term.move(4, 0)}└────┘'
        )

    def test_as_str_with_frame_color_different_than_content(
        self, capsys, term
    ):
        """When converted to a string, a Pane object returns a string
        that will draw the entire splash screen.
        """
        panel = p.Frame(
            height=5,
            width=6,
            bg='red',
            fg='blue',
            frame_type='light',
            frame_bg='green',
            frame_fg='white'
        )
        assert str(panel) == (
            f'{term.blue_on_red}'
            f'{term.move(1, 1)}    '
            f'{term.move(2, 1)}    '
            f'{term.move(3, 1)}    '
            f'{term.normal}'
            f'{term.white_on_green}'
            f'{term.move(0, 0)}┌────┐'
            f'{term.move(1, 0)}│'
            f'{term.move(1, 5)}│'
            f'{term.move(2, 0)}│'
            f'{term.move(2, 5)}│'
            f'{term.move(3, 0)}│'
            f'{term.move(3, 5)}│'
            f'{term.move(4, 0)}└────┘'
            f'{term.normal}'
        )

    def test_as_str_with_panel_pad(self, capsys, term):
        """When converted to a string, a Pane object returns a string
        that will draw the entire splash screen. If padding is set for
        the panel, the panel should be inset by that amount.
        """
        panel = p.Frame(
            height=10,
            width=10,
            frame_type='light',
            panel_pad_bottom=0.3,
            panel_pad_left=0.1,
            panel_pad_right=0.3,
            panel_pad_top=0.2
        )
        assert str(panel) == (
            f'{term.move(3, 2)}    '
            f'{term.move(4, 2)}    '
            f'{term.move(5, 2)}    '
            f'{term.move(2, 1)}┌────┐'
            f'{term.move(3, 1)}│'
            f'{term.move(3, 6)}│'
            f'{term.move(4, 1)}│'
            f'{term.move(4, 6)}│'
            f'{term.move(5, 1)}│'
            f'{term.move(5, 6)}│'
            f'{term.move(6, 1)}└────┘'
        )

    def test_as_str_with_panel_pad_left_rel_width(self, capsys, term):
        """When converted to a string, a Pane object returns a string
        that will draw the entire splash screen. If padding left and
        relative width are set for the panel, the panel should be inset
        by the correct amount.
        """
        panel = p.Frame(
            height=5,
            width=10,
            panel_pad_left=0.1,
            panel_relative_width=0.6,
            frame_type='light'
        )
        assert str(panel) == (
            f'{term.move(1, 2)}    '
            f'{term.move(2, 2)}    '
            f'{term.move(3, 2)}    '
            f'{term.move(0, 1)}┌────┐'
            f'{term.move(1, 1)}│'
            f'{term.move(1, 6)}│'
            f'{term.move(2, 1)}│'
            f'{term.move(2, 6)}│'
            f'{term.move(3, 1)}│'
            f'{term.move(3, 6)}│'
            f'{term.move(4, 1)}└────┘'
        )

    def test_as_str_with_panel_pad_right_rel_width(self, capsys, term):
        """When converted to a string, a Pane object returns a string
        that will draw the entire splash screen. If padding right and
        relative width are set for the panel, the panel should be inset
        by the correct amount.
        """
        panel = p.Frame(
            height=5,
            width=10,
            panel_pad_right=0.3,
            panel_relative_width=0.6,
            frame_type='light'
        )
        assert str(panel) == (
            f'{term.move(1, 2)}    '
            f'{term.move(2, 2)}    '
            f'{term.move(3, 2)}    '
            f'{term.move(0, 1)}┌────┐'
            f'{term.move(1, 1)}│'
            f'{term.move(1, 6)}│'
            f'{term.move(2, 1)}│'
            f'{term.move(2, 6)}│'
            f'{term.move(3, 1)}│'
            f'{term.move(3, 6)}│'
            f'{term.move(4, 1)}└────┘'
        )

    def test_as_str_with_panel_rel_dim(self, capsys, term):
        """When converted to a string, a Pane object returns a string
        that will draw the entire splash screen. If relative dimensions
        are set on the panel, the height and width should be offset by
        that amount.
        """
        panel = p.Frame(
            height=10,
            width=10,
            panel_relative_height=0.5,
            panel_relative_width=0.6,
            frame_type='light'
        )
        assert str(panel) == (
            f'{term.move(3, 3)}    '
            f'{term.move(4, 3)}    '
            f'{term.move(5, 3)}    '
            f'{term.move(6, 3)}    '
            f'{term.move(2, 2)}┌────┐'
            f'{term.move(3, 2)}│'
            f'{term.move(3, 7)}│'
            f'{term.move(4, 2)}│'
            f'{term.move(4, 7)}│'
            f'{term.move(5, 2)}│'
            f'{term.move(5, 7)}│'
            f'{term.move(6, 2)}│'
            f'{term.move(6, 7)}│'
            f'{term.move(7, 2)}└────┘'
        )

    def test_as_str_with_panel_rel_dims_and_align_h_left(self, capsys, term):
        """When converted to a string, a Pane object returns a string
        that will draw the entire splash screen. If relative dimensions
        are set on the panel, the height and width should be offset by
        that amount.
        """
        panel = p.Frame(
            height=10,
            width=10,
            panel_relative_height=0.5,
            panel_relative_width=0.6,
            panel_align_h='left',
            frame_type='light'
        )
        assert str(panel) == (
            f'{term.move(3, 1)}    '
            f'{term.move(4, 1)}    '
            f'{term.move(5, 1)}    '
            f'{term.move(6, 1)}    '
            f'{term.move(2, 0)}┌────┐'
            f'{term.move(3, 0)}│'
            f'{term.move(3, 5)}│'
            f'{term.move(4, 0)}│'
            f'{term.move(4, 5)}│'
            f'{term.move(5, 0)}│'
            f'{term.move(5, 5)}│'
            f'{term.move(6, 0)}│'
            f'{term.move(6, 5)}│'
            f'{term.move(7, 0)}└────┘'
        )

    def test_as_str_with_panel_rel_dims_and_align_h_right(self, capsys, term):
        """When converted to a string, a Pane object returns a string
        that will draw the entire splash screen. If relative dimensions
        are set on the panel, the height and width should be offset by
        that amount.
        """
        panel = p.Frame(
            height=10,
            width=10,
            panel_relative_height=0.5,
            panel_relative_width=0.6,
            panel_align_h='right',
            frame_type='light'
        )
        assert str(panel) == (
            f'{term.move(3, 5)}    '
            f'{term.move(4, 5)}    '
            f'{term.move(5, 5)}    '
            f'{term.move(6, 5)}    '
            f'{term.move(2, 4)}┌────┐'
            f'{term.move(3, 4)}│'
            f'{term.move(3, 9)}│'
            f'{term.move(4, 4)}│'
            f'{term.move(4, 9)}│'
            f'{term.move(5, 4)}│'
            f'{term.move(5, 9)}│'
            f'{term.move(6, 4)}│'
            f'{term.move(6, 9)}│'
            f'{term.move(7, 4)}└────┘'
        )

    def test_as_str_with_panel_rel_dims_and_align_v_bottom(
        self, capsys, term
    ):
        """When converted to a string, a Pane object returns a string
        that will draw the entire splash screen. If relative dimensions
        are set on the panel, the height and width should be offset by
        that amount.
        """
        panel = p.Frame(
            height=10,
            width=10,
            panel_relative_height=0.5,
            panel_relative_width=0.6,
            panel_align_v='bottom',
            frame_type='light'
        )
        assert str(panel) == (
            f'{term.move(6, 3)}    '
            f'{term.move(7, 3)}    '
            f'{term.move(8, 3)}    '
            f'{term.move(5, 2)}┌────┐'
            f'{term.move(6, 2)}│'
            f'{term.move(6, 7)}│'
            f'{term.move(7, 2)}│'
            f'{term.move(7, 7)}│'
            f'{term.move(8, 2)}│'
            f'{term.move(8, 7)}│'
            f'{term.move(9, 2)}└────┘'
        )

    def test_as_str_with_panel_rel_dims_and_align_v_top(
        self, capsys, term
    ):
        """When converted to a string, a Pane object returns a string
        that will draw the entire splash screen. If relative dimensions
        are set on the panel, the height and width should be offset by
        that amount.
        """
        panel = p.Frame(
            height=10,
            width=10,
            panel_relative_height=0.5,
            panel_relative_width=0.6,
            panel_align_v='top',
            frame_type='light'
        )
        assert str(panel) == (
            f'{term.move(1, 3)}    '
            f'{term.move(2, 3)}    '
            f'{term.move(3, 3)}    '
            f'{term.move(0, 2)}┌────┐'
            f'{term.move(1, 2)}│'
            f'{term.move(1, 7)}│'
            f'{term.move(2, 2)}│'
            f'{term.move(2, 7)}│'
            f'{term.move(3, 2)}│'
            f'{term.move(3, 7)}│'
            f'{term.move(4, 2)}└────┘'
        )

    def test_clear_contents(self, capsys, term):
        """When called, Panel.clear_contents will return a string that
        clears the area within the panel in the terminal. If there is
        a frame set for the panel, the cleared area should not affect
        the frame.
        """
        panel = p.Frame(
            height=5,
            width=6,
            frame_type='light'
        )
        assert panel.clear_contents() == (
            f'{term.move(1, 1)}    '
            f'{term.move(2, 1)}    '
            f'{term.move(3, 1)}    '
        )

    def test_frame(self, capsys, term):
        """When referenced, the Panel.frame property should return a
        string that will draw the panel's frame in the terminal.
        """
        panel = p.Frame(
            height=5,
            width=6,
            frame_type='light'
        )
        assert panel.frame == (
            f'{term.move(0, 0)}┌────┐'
            f'{term.move(1, 0)}│'
            f'{term.move(1, 5)}│'
            f'{term.move(2, 0)}│'
            f'{term.move(2, 5)}│'
            f'{term.move(3, 0)}│'
            f'{term.move(3, 5)}│'
            f'{term.move(4, 0)}└────┘'
        )


class TestPanel:
    def test__init_default(self, panel_attr_defaults):
        """Given only the required parameters, a Panel subclass should
        return an object with the expected attributes set.
        """
        panel = p.Panel()
        assert {
            k: getattr(panel, k) for k in panel_attr_defaults
        } == panel_attr_defaults

    def test__init_set(self, panel_attr_set):
        """Given any parameters, a Panel subclass should return an
        object with the expected attributes set.
        """
        panel = p.Panel(**panel_attr_set)
        assert {
            k: getattr(panel, k) for k in panel_attr_set
        } == panel_attr_set

    def test__init_cannot_set_panel_pad_left_and_align_h(self):
        """If `panel_pad_left` and `panel_align_h` are set, raise
        a PanelPaddingAndAlignmentSetError.
        """
        with pt.raises(p.PanelPaddingAndAlignmentSetError):
            _ = p.Panel(panel_pad_left=0.1, panel_align_h='left')

    def test__init_cannot_set_panel_pad_right_and_align_h(self):
        """If `panel_pad_right` and `panel_align_h` are set, raise
        a PanelPaddingAndAlignmentSetError.
        """
        with pt.raises(p.PanelPaddingAndAlignmentSetError):
            _ = p.Panel(panel_pad_right=0.1, panel_align_h='left')

    def test__init_sum_of_h_rel_dims_does_not_equal_one(self):
        """If `panel_pad_left`, `panel_pad_right`, and
        `panel_relative_width` are set but the sum of all
        three doesn't equal one, `Panel` should raise a
        `panel.InvalidDimensionsError` exception.
        """
        with pt.raises(p.InvalidDimensionsError):
            _ = p.Panel(
                panel_pad_left=0.1,
                panel_pad_right=0.2,
                panel_relative_width=0.3
            )

    def test__init_sum_of_v_rel_dims_does_not_equal_one(self):
        """If `panel_pad_bottom`, `panel_pad_top`, and
        `panel_relative_height` are set but the sum of all
        three doesn't equal one, `Panel` should raise a
        `panel.InvalidDimensionsError` exception.
        """
        with pt.raises(p.InvalidDimensionsError):
            _ = p.Panel(
                panel_pad_bottom=0.1,
                panel_pad_top=0.2,
                panel_relative_height=0.3
            )

    def test_as_str(self, capsys, term):
        """When converted to a string, a Pane object returns a string
        that will draw the entire splash screen.
        """
        panel = p.Panel(
            height=5,
            width=6
        )
        assert str(panel) == (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
        )

    def test_as_str_with_bg_and_fg(self, capsys, term):
        """When converted to a string, a Pane object returns a string
        that will draw the entire splash screen. If there are foreground
        and background colors, the contents of the pane should have
        those colors.
        """
        panel = p.Panel(
            height=5,
            width=6,
            bg='blue',
            fg='red'
        )
        assert str(panel) == (
            f'{term.red_on_blue}'
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.normal}'
        )

    def test_action(self, KEY_ENTER):
        """If passed a keystroke, Panel.action() should return a tuple
        containing the string for the keystroke and an empty string.
        """
        panel = p.Panel(
            height=5,
            width=6
        )
        assert panel.action(KEY_ENTER) == ('\n', '')

    def test_clear_contents(self, capsys, term):
        """When called, Panel.clear_contents will return a string that
        clears the area within the panel in the terminal.
        """
        panel = p.Panel(
            height=5,
            width=6
        )
        assert panel.clear_contents() == (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
        )

    def test_clear_contents_with_bg(self, capsys, term):
        """When called, Panel.clear_contents will return a string that
        clears the area within the panel in the terminal. If there is a
        background color, the cleared area should have that color.
        """
        panel = p.Panel(
            height=5,
            width=6,
            bg='blue'
        )
        assert panel.clear_contents() == (
            f'{term.on_blue}'
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.normal}'
        )

    def test_clear_contents_with_bg_and_fg(self, capsys, term):
        """When called, Panel.clear_contents will return a string that
        clears the area within the panel in the terminal. If there are
        background and foreground colors, the cleared area should have
        those colors.
        """
        panel = p.Panel(
            height=5,
            width=6,
            bg='blue',
            fg='red'
        )
        assert panel.clear_contents() == (
            f'{term.red_on_blue}'
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.normal}'
        )

    def test_clear_contents_with_fg(self, capsys, term):
        """When called, Panel.clear_contents will return a string that
        clears the area within the panel in the terminal. If there is a
        foreground color, the cleared area should have that color.
        """
        panel = p.Panel(
            height=5,
            width=6,
            fg='blue'
        )
        assert panel.clear_contents() == (
            f'{term.blue}'
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.normal}'
        )

    def test_register_key(self):
        """Given a string with the name of a control key as used by
        :mod:blessed and a method that follows the action handler
        protocol, :meth:Panel.register_key() should add the key and
        method to the dictionary of active keys.
        """
        def spam(self, key=None) -> str:
            return ''

        panel = p.Panel(
            height=5,
            width=6
        )
        setattr(panel, 'spam', spam)
        panel.register_key('KEY_SPAM', spam)
        assert panel.active_keys == {'KEY_SPAM': spam,}

    def test_register_key_given_unbound_method(self):
        """Given a string with the name of a control key as used by
        :mod:blessed and a method that follows the action handler
        protocol, :meth:Panel.register_key() should add the key and
        method to the dictionary of active keys. If the callable is
        not a bound method of the :class:Panel object, the callable
        should be bound as a method to the panel before it is added
        to the dictionary of active keys.
        """
        def spam(self, key=None) -> str:
            return ''

        panel = p.Panel(
            height=5,
            width=6
        )
        panel.register_key('KEY_SPAM', spam)
        assert panel.active_keys == {'KEY_SPAM': spam,}

    def test_register_key_given_unbound_method(self):
        """If passed a message, Panel.update() should return an empty
        string.
        """
        @dataclass
        class Spam(Message):
            value: str

        msg = Spam('eggs')
        panel = p.Panel(
            height=5,
            width=6
        )
        assert panel.update(msg) == ''


class TestTitle:
    def test__init_default(
        self, title_attr_defaults,
        frame_attr_defaults,
        panel_attr_defaults
    ):
        """Given only the required parameters, a Title should
        return an object with the expected attributes set.
        """
        panel = p.Title()
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
        self, title_attr_set,
        frame_attr_set,
        panel_attr_set
    ):
        """Given any parameters, a Title should return an
        object with the expected attributes set.
        """
        panel = p.Title(
            **title_attr_set,
            **frame_attr_set,
            **panel_attr_set
        )
        assert {
            k: getattr(panel, k) for k in title_attr_set
        } == title_attr_set
        assert {
            k: getattr(panel, k) for k in frame_attr_set
        } == frame_attr_set
        assert {
            k: getattr(panel, k) for k in panel_attr_set
        } == panel_attr_set

    def test__init_footer_frame_no_frame_type(self):
        """If the footer_frame attribute is set without setting the
        frame_type attribute, the `Title` object should raise a
        `panel.NoFrameTypeForFrameError`.
        """
        with pt.raises(p.NoFrameTypeForFrameError):
            _ = p.Title(
                footer_text='spam',
                footer_frame=True,
                height=7,
                width=10
            )

    def test__init_title_frame_no_frame_type(self):
        """If the title_frame attribute is set without setting the
        title_type attribute, the `Title` object should raise a
        `panel.NoFrameTypeForFrameError`.
        """
        with pt.raises(p.NoFrameTypeForFrameError):
            _ = p.Title(
                title_text='spam',
                title_frame=True,
                height=7,
                width=10
            )

    def test_as_str(self, term):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen.
        """
        panel = p.Title(
            title_text='spam',
            height=5,
            width=6
        )
        assert str(panel) == (
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(0, 0)}      '
            f'{term.move(0, 0)}spam'
        )

    def test_as_str_with_bg(self, term):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If the background
        color is set, the title should be that color.
        """
        panel = p.Title(
            title_text='spam',
            height=5,
            width=6,
            bg='red'
        )
        assert str(panel) == (
            f'{term.on_red}'
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.normal}'
            f'{term.on_red}'
            f'{term.move(0, 0)}      '
            f'{term.normal}'
            f'{term.move(0, 0)}'
            f'{term.on_red}'
            'spam'
            f'{term.normal}'
        )

    def test_as_str_with_fg(self, term):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If the foreground
        color is set, the title should be that color.
        """
        panel = p.Title(
            title_text='spam',
            height=5,
            width=6,
            fg='red'
        )
        assert str(panel) == (
            f'{term.red}'
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.normal}'
            f'{term.red}'
            f'{term.move(0, 0)}      '
            f'{term.normal}'
            f'{term.move(0, 0)}'
            f'{term.red}'
            'spam'
            f'{term.normal}'
        )

    def test_as_str_with_footer(self, term):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If there is a
        footer, it appears on the bottom of the panel.
        """
        panel = p.Title(
            footer_text='spam',
            height=5,
            width=6
        )
        assert str(panel) == (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(4, 0)}spam'
        )

    def test_as_str_with_footer_align_center(self, term):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If there is a
        footer, it appears on the bottom of the panel. If there the
        footer align is center, the footer is center of the bottom line
        of the panel.
        """
        panel = p.Title(
            footer_text='spam',
            footer_align='center',
            height=5,
            width=10
        )
        assert str(panel) == (
            f'{term.move(0, 0)}          '
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(4, 0)}          '
            f'{term.move(4, 3)}spam'
        )

    def test_as_str_with_footer_align_right(self, term):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If there is a
        footer, it appears on the bottom of the panel. If there the
        footer align is right, the footer on the right of the bottom
        line of the panel.
        """
        panel = p.Title(
            footer_text='spam',
            footer_align='right',
            height=5,
            width=10
        )
        assert str(panel) == (
            f'{term.move(0, 0)}          '
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(4, 0)}          '
            f'{term.move(4, 6)}spam'
        )

    def test_as_str_with_footer_align_right_and_panel_pad_right(self, term):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If there is a
        footer, it appears on the bottom of the panel. If there the
        footer align is right, the footer on the right of the bottom
        line of the panel. If there is right panel padding, the footer
        should be offset the correct amount.
        """
        panel = p.Title(
            footer_text='spam',
            footer_align='right',
            panel_pad_right=0.5,
            height=5,
            width=20
        )
        assert str(panel) == (
            f'{term.move(0, 0)}          '
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(4, 0)}          '
            f'{term.move(4, 6)}spam'
        )

    def test_as_str_with_footer_frame(self, term):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If there is a
        footer, it appears on the bottom of the panel. If there is a
        footer frame, the frame is capped on either side of the footer.
        """
        panel = p.Title(
            footer_text='spam',
            footer_frame=True,
            frame_type='light',
            height=7,
            width=10
        )
        assert str(panel) == (
            f'{term.move(1, 1)}        '
            f'{term.move(2, 1)}        '
            f'{term.move(3, 1)}        '
            f'{term.move(4, 1)}        '
            f'{term.move(5, 1)}        '
            f'{term.move(0, 0)}┌────────┐'
            f'{term.move(1, 0)}│'
            f'{term.move(1, 9)}│'
            f'{term.move(2, 0)}│'
            f'{term.move(2, 9)}│'
            f'{term.move(3, 0)}│'
            f'{term.move(3, 9)}│'
            f'{term.move(4, 0)}│'
            f'{term.move(4, 9)}│'
            f'{term.move(5, 0)}│'
            f'{term.move(5, 9)}│'
            f'{term.move(6, 0)}└────────┘'
            f'{term.move(6, 1)}┤spam├'
        )

    def test_as_str_with_footer_and_panel_pad_bottom(self, term):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If there is a
        footer, it appears on the bottom of the panel. If there is
        bottom panel padding, the location of the footer should be
        offset correctly.
        """
        panel = p.Title(
            footer_text='spam',
            panel_pad_bottom=0.5,
            height=10,
            width=6
        )
        assert str(panel) == (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(4, 0)}spam'
        )

    def test_as_str_with_frame(self, term):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If the panel
        has a frame, the title should be on the top line of the frame,
        indented to match left margin of the contents.
        """
        panel = p.Title(
            title_text='spam',
            frame_type='light',
            height=5,
            width=10
        )
        assert str(panel) == (
            f'{term.move(1, 1)}        '
            f'{term.move(2, 1)}        '
            f'{term.move(3, 1)}        '
            f'{term.move(0, 0)}┌────────┐'
            f'{term.move(1, 0)}│'
            f'{term.move(1, 9)}│'
            f'{term.move(2, 0)}│'
            f'{term.move(2, 9)}│'
            f'{term.move(3, 0)}│'
            f'{term.move(3, 9)}│'
            f'{term.move(4, 0)}└────────┘'
            f'{term.move(0, 1)}spam'
        )

    def test_as_str_with_frame_and_frame_bg_and_title_frame(self, term):
        """When converted to a string, a `Title` object returns a
        string that will draw the panel. If the panel has a frame,
        the title should be on the top line of the frame, indented
        to match left margin of the contents. If the frame has a
        color, the frame should be that color. If the title has a
        frame, the frame should be capped on either side ot the title,
        and the cap should be the same color as the frame.
        """
        panel = p.Title(
            title_text='spam',
            title_frame=True,
            frame_type='light',
            frame_fg='red',
            frame_bg='blue',
            height=5,
            width=10
        )
        assert str(panel) == (
            f'{term.move(1, 1)}        '
            f'{term.move(2, 1)}        '
            f'{term.move(3, 1)}        '
            f'{term.red_on_blue}'
            f'{term.move(0, 0)}┌────────┐'
            f'{term.move(1, 0)}│'
            f'{term.move(1, 9)}│'
            f'{term.move(2, 0)}│'
            f'{term.move(2, 9)}│'
            f'{term.move(3, 0)}│'
            f'{term.move(3, 9)}│'
            f'{term.move(4, 0)}└────────┘'
            f'{term.normal}'
            f'{term.move(0, 1)}'
            f'{term.red_on_blue}'
            '┤'
            f'{term.normal}'
            'spam'
            f'{term.red_on_blue}'
            '├'
            f'{term.normal}'
        )

    def test_as_str_with_frame_and_overflowing_title(self, term):
        """When converted to a string, a `Title` object returns a
        string that will draw the panel. If the panel has a frame,
        the title should be on the top line of the frame, indented
        to match left margin of the contents. If the frame has a
        color, the frame should be that color. If the title has a
        frame, the frame should be capped on either side ot the title,
        and the cap should be the same color as the frame.
        """
        panel = p.Title(
            title_text='spameggsbacon',
            frame_type='light',
            height=5,
            width=10
        )
        assert str(panel) == (
            f'{term.move(1, 1)}        '
            f'{term.move(2, 1)}        '
            f'{term.move(3, 1)}        '
            f'{term.move(0, 0)}┌────────┐'
            f'{term.move(1, 0)}│'
            f'{term.move(1, 9)}│'
            f'{term.move(2, 0)}│'
            f'{term.move(2, 9)}│'
            f'{term.move(3, 0)}│'
            f'{term.move(3, 9)}│'
            f'{term.move(4, 0)}└────────┘'
            f'{term.move(0, 1)}spame[▸]'
        )

    def test_as_str_with_overflowing_footer(self, term):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If there is a
        footer, it appears on the bottom of the panel. If the footer
        is longer than the available space, the footer is truncated and
        the overflow indicator is added.
        """
        panel = p.Title(
            footer_text='spameggs',
            height=5,
            width=6
        )
        assert str(panel) == (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(4, 0)}spa[▸]'
        )


@pt.mark.skip
class TitleTestCase(TerminalTestCase):
    def test___str__with_overflowing_title(self):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If the title
        is longer than the available space, the title is truncated and
        the overflow indicator is added.
        """
        # Expected values.
        exp = (
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(0, 0)}      '
            f'{term.move(0, 0)}spa[▸]'
        )

        # Test data and state.
        kwargs = {
            'title_text': 'spameggs',
            'height': 5,
            'width': 6,
            'term': term,
        }
        panel = p.Title(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_panel_pad_left(self):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If there is
        left panel padding, the location of the title should be offset
        by the correct amount.
        """
        # Expected values.
        exp = (
            f'{term.move(1, 4)}      '
            f'{term.move(2, 4)}      '
            f'{term.move(3, 4)}      '
            f'{term.move(4, 4)}      '
            f'{term.move(0, 4)}      '
            f'{term.move(0, 4)}spam'
        )

        # Test data and state.
        kwargs = {
            'title_text': 'spam',
            'panel_pad_left': 0.4,
            'height': 5,
            'width': 10,
            'term': term,
        }
        panel = p.Title(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_panel_pad_top(self):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If there is
        top panel padding, the location of the title should be offset
        by the correct amount.
        """
        # Expected values.
        exp = (
            f'{term.move(6, 0)}      '
            f'{term.move(7, 0)}      '
            f'{term.move(8, 0)}      '
            f'{term.move(9, 0)}      '
            f'{term.move(5, 0)}      '
            f'{term.move(5, 0)}spam'
        )

        # Test data and state.
        kwargs = {
            'title_text': 'spam',
            'panel_pad_top': 0.5,
            'height': 10,
            'width': 6,
            'term': term,
        }
        panel = p.Title(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_title_align_center(self):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If the title
        is aligned to the center, the title should be indented to move
        it to the center of the top line of the panel.
        """
        # Expected values.
        exp = (
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(4, 0)}          '
            f'{term.move(0, 0)}          '
            f'{term.move(0, 3)}spam'
        )

        # Test data and state.
        kwargs = {
            'title_text': 'spam',
            'title_align': 'center',
            'height': 5,
            'width': 10,
            'term': term,
        }
        panel = p.Title(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_title_align_error(self):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If the string
        for the title alignment isn't recognized, the object should
        raise a TitleAlignmentError.
        """
        # Expected values.
        exp_ex = p.InvalidTitleAlignmentError
        exp_msg = 'Invalid title alignment: eggs.'

        # Test data and state.
        kwargs = {
            'title_text': 'spam',
            'title_align': 'eggs',
            'height': 5,
            'width': 10,
            'term': term,
        }
        panel = p.Title(**kwargs)

        # Run test and determine test results.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = str(panel)

    def test___str__with_title_align_right(self):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If the title
        is aligned to the center, the title should be indented to move
        it to the right of the top line of the panel.
        """
        # Expected values.
        exp = (
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(4, 0)}          '
            f'{term.move(0, 0)}          '
            f'{term.move(0, 6)}spam'
        )

        # Test data and state.
        kwargs = {
            'title_text': 'spam',
            'title_align': 'right',
            'height': 5,
            'width': 10,
            'term': term,
        }
        panel = p.Title(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_title_bg(self):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If the title
        background color is set, the title should be that color.
        """
        # Expected values.
        exp = (
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.on_red}'
            f'{term.move(0, 0)}      '
            f'{term.normal}'
            f'{term.move(0, 0)}'
            f'{term.on_red}'
            'spam'
            f'{term.normal}'
        )

        # Test data and state.
        kwargs = {
            'title_text': 'spam',
            'title_bg': 'red',
            'height': 5,
            'width': 6,
            'term': term,
        }
        panel = p.Title(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_title_bg_and_bg(self):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If the title
        background and background colors are set, the title should be
        the title background color.
        """
        # Expected values.
        exp = (
            f'{term.on_red}'
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.normal}'
            f'{term.on_blue}'
            f'{term.move(0, 0)}      '
            f'{term.normal}'
            f'{term.move(0, 0)}'
            f'{term.on_blue}'
            'spam'
            f'{term.normal}'
        )

        # Test data and state.
        kwargs = {
            'title_text': 'spam',
            'title_bg': 'blue',
            'height': 5,
            'width': 6,
            'term': term,
            'bg': 'red',
        }
        panel = p.Title(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_title_fg(self):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If the title
        foreground color is set, the title should be that color.
        """
        # Expected values.
        exp = (
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.red}'
            f'{term.move(0, 0)}      '
            f'{term.normal}'
            f'{term.move(0, 0)}'
            f'{term.red}'
            'spam'
            f'{term.normal}'
        )

        # Test data and state.
        kwargs = {
            'title_text': 'spam',
            'title_fg': 'red',
            'height': 5,
            'width': 6,
            'term': term,
        }
        panel = p.Title(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_title_fg_and_fg(self):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If the title
        foreground and foreground colors are set, the title should be
        the title foreground color.
        """
        # Expected values.
        exp = (
            f'{term.red}'
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.normal}'
            f'{term.blue}'
            f'{term.move(0, 0)}      '
            f'{term.normal}'
            f'{term.move(0, 0)}'
            f'{term.blue}'
            'spam'
            f'{term.normal}'
        )

        # Test data and state.
        kwargs = {
            'title_text': 'spam',
            'title_fg': 'blue',
            'height': 5,
            'width': 6,
            'term': term,
            'fg': 'red',
        }
        panel = p.Title(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_title_frame(self):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If there is a
        title frame, the frame is capped on either side of the title.
        """
        # Expected values.
        exp = (
            f'{term.move(1, 1)}        '
            f'{term.move(2, 1)}        '
            f'{term.move(3, 1)}        '
            f'{term.move(4, 1)}        '
            f'{term.move(5, 1)}        '
            f'{term.move(0, 0)}┌────────┐'
            f'{term.move(1, 0)}│'
            f'{term.move(1, 9)}│'
            f'{term.move(2, 0)}│'
            f'{term.move(2, 9)}│'
            f'{term.move(3, 0)}│'
            f'{term.move(3, 9)}│'
            f'{term.move(4, 0)}│'
            f'{term.move(4, 9)}│'
            f'{term.move(5, 0)}│'
            f'{term.move(5, 9)}│'
            f'{term.move(6, 0)}└────────┘'
            f'{term.move(0, 1)}┤spam├'
        )

        # Test data and state.
        kwargs = {
            'title_text': 'spam',
            'title_frame': True,
            'frame_type': 'light',
            'height': 7,
            'width': 10,
            'term': term,
        }
        panel = p.Title(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_title_frame_and_panel_pad_top_left(self):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If there is a
        title frame, the frame is capped on either side of the title.
        """
        # Expected values.
        exp = (
            f'{term.move(4, 11)}        '
            f'{term.move(5, 11)}        '
            f'{term.move(6, 11)}        '
            f'{term.move(7, 11)}        '
            f'{term.move(8, 11)}        '
            f'{term.move(3, 10)}┌────────┐'
            f'{term.move(4, 10)}│'
            f'{term.move(4, 19)}│'
            f'{term.move(5, 10)}│'
            f'{term.move(5, 19)}│'
            f'{term.move(6, 10)}│'
            f'{term.move(6, 19)}│'
            f'{term.move(7, 10)}│'
            f'{term.move(7, 19)}│'
            f'{term.move(8, 10)}│'
            f'{term.move(8, 19)}│'
            f'{term.move(9, 10)}└────────┘'
            f'{term.move(3, 11)}┤spam├'
        )

        # Test data and state.
        kwargs = {
            'title_text': 'spam',
            'title_frame': True,
            'frame_type': 'light',
            'panel_pad_top': 0.3,
            'panel_pad_left': 0.5,
            'height': 10,
            'width': 20,
            'term': term,
        }
        panel = p.Title(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)
