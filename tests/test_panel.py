"""
test_panel
~~~~~~~~~~

Unit tests for the `thurible.panel` module.
"""
import unittest as ut

from blessed import Terminal
from blessed.keyboard import Keystroke

from thurible import panel as p


# Common values.
term = Terminal()
kwargs_content_opt_default = {
    'content_align_h': 'center',
    'content_align_v': 'middle',
    'content_pad_left': 0.0,
    'content_pad_right': 0.0,
}
kwargs_content_opt_default_alt = kwargs_content_opt_default.copy()
kwargs_content_opt_default_alt['content_align_h'] = 'left'
kwargs_content_opt_default_alt['content_align_v'] = 'top'
kwargs_content_opt_set = {
    'content_align_h': 'right',
    'content_align_v': 'bottom',
    'content_pad_left': 0.2,
    'content_pad_right': 0.2,
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
    'origin_y': 0,
    'origin_x': 0,
    'fg': '',
    'bg': '',
}
kwargs_panel_opt_set = {
    'height': 5,
    'width': 7,
    'term': term,
    'origin_y': 2,
    'origin_x': 3,
    'fg': 'red',
    'bg': 'blue',
}
kwargs_panel_req = {
    'height': 5,
    'width': 7,
    'term': term,
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
class PanelTestCase(TerminalTestCase):
    def test___init__optional_parameters(self):
        """Given any parameters, a Panel subclass should return an
        object with the expected attributes set.
        """
        # Expected values.
        exp = {
            **kwargs_frame_opt_set,
            **kwargs_panel_opt_set,
        }

        # Run test.
        panel = p.Panel(**exp)

        # Gather actuals.
        act = {key: getattr(panel, key) for key in exp}

        # Determine test results.
        self.assertDictEqual(exp, act)

    def test___init__required_parameters(self):
        """Given only the required parameters, a Panel subclass should
        return an object with the expected attributes set.
        """
        # Expected values.
        exp_req = kwargs_panel_req
        exp_opt = {
            **kwargs_frame_opt_default,
            **kwargs_panel_opt_default
        }

        # Run test.
        panel = p.Panel(**exp_req)

        # Gather actuals.
        act_req = {key: getattr(panel, key) for key in exp_req}
        act_opt = {key: getattr(panel, key) for key in exp_opt}

        # Determine test results.
        self.assertDictEqual(exp_req, act_req)
        self.assertDictEqual(exp_opt, act_opt)

    def test___str__(self):
        """When converted to a string, a Pane object returns a string
        that will draw the entire splash screen.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
        )

        # Test data and state.
        kwargs = {
            'height': 5,
            'width': 6,
            'term': term,
        }
        panel = p.Panel(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_bg_and_fg(self):
        """When converted to a string, a Pane object returns a string
        that will draw the entire splash screen. If there are foreground
        and background colors, the contents of the pane should have
        those colors.
        """
        # Expected values.
        exp = (
            f'{term.red_on_blue}'
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.normal}'
        )

        # Test data and state.
        kwargs = {
            'height': 5,
            'width': 6,
            'term': term,
            'bg': 'blue',
            'fg': 'red',
        }
        panel = p.Panel(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_frame(self):
        """When converted to a string, a Pane object returns a string
        that will draw the entire splash screen.
        """
        # Expected values.
        exp = (
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

        # Test data and state.
        kwargs = {
            'height': 5,
            'width': 6,
            'term': term,
            'frame_type': 'light',
        }
        panel = p.Panel(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_frame_and_frame_color_different_than_content(self):
        """When converted to a string, a Pane object returns a string
        that will draw the entire splash screen.
        """
        # Expected values.
        exp = (
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

        # Test data and state.
        kwargs = {
            'height': 5,
            'width': 6,
            'term': term,
            'bg': 'red',
            'fg': 'blue',
            'frame_type': 'light',
            'frame_bg': 'green',
            'frame_fg': 'white',
        }
        panel = p.Panel(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_action(self):
        """If passed a keystroke, Panel.action() should return a tuple
        containing the string for the keystroke and an empty string.
        """
        # Expected values.
        exp = ('\n', '')

        # Test data and state.
        kwargs = {
            'height': 5,
            'width': 6,
            'term': term,
        }
        panel = p.Panel(**kwargs)
        key = Keystroke('\n', term.KEY_ENTER, 'KEY_ENTER')

        # Run test.
        act = panel.action(key)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_clear_contents(self):
        """When called, Panel.clear_contents will return a string that
        clears the area within the panel in the terminal.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
        )

        # Test data and state.
        kwargs = {
            'height': 5,
            'width': 6,
            'term': term,
        }
        panel = p.Panel(**kwargs)

        # Run test.
        act = panel.clear_contents()

        # Determine test result.
        self.assertEqual(exp, act)

    def test_clear_contents_with_bg(self):
        """When called, Panel.clear_contents will return a string that
        clears the area within the panel in the terminal. If there is a
        background color, the cleared area should have that color.
        """
        # Expected values.
        exp = (
            f'{term.on_blue}'
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.normal}'
        )

        # Test data and state.
        kwargs = {
            'height': 5,
            'width': 6,
            'term': term,
            'bg': 'blue',
        }
        panel = p.Panel(**kwargs)

        # Run test.
        act = panel.clear_contents()

        # Determine test result.
        self.assertEqual(exp, act)

    def test_clear_contents_with_bg_and_fg(self):
        """When called, Panel.clear_contents will return a string that
        clears the area within the panel in the terminal. If there are
        background and foreground colors, the cleared area should have
        those colors.
        """
        # Expected values.
        exp = (
            f'{term.red_on_blue}'
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.normal}'
        )

        # Test data and state.
        kwargs = {
            'height': 5,
            'width': 6,
            'term': term,
            'bg': 'blue',
            'fg': 'red',
        }
        panel = p.Panel(**kwargs)

        # Run test.
        act = panel.clear_contents()

        # Determine test result.
        self.assertEqual(exp, act)

    def test_clear_contents_with_frame(self):
        """When called, Panel.clear_contents will return a string that
        clears the area within the panel in the terminal. If there is
        a frame set for the panel, the cleared area should not affect
        the frame.
        """
        # Expected values.
        exp = (
            f'{term.move(1, 1)}    '
            f'{term.move(2, 1)}    '
            f'{term.move(3, 1)}    '
        )

        # Test data and state.
        kwargs = {
            'height': 5,
            'width': 6,
            'term': term,
            'frame_type': 'light',
        }
        panel = p.Panel(**kwargs)

        # Run test.
        act = panel.clear_contents()

        # Determine test result.
        self.assertEqual(exp, act)

    def test_clear_contents_with_fg(self):
        """When called, Panel.clear_contents will return a string that
        clears the area within the panel in the terminal. If there is a
        foreground color, the cleared area should have that color.
        """
        # Expected values.
        exp = (
            f'{term.blue}'
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.normal}'
        )

        # Test data and state.
        kwargs = {
            'height': 5,
            'width': 6,
            'term': term,
            'fg': 'blue',
        }
        panel = p.Panel(**kwargs)

        # Run test.
        act = panel.clear_contents()

        # Determine test result.
        self.assertEqual(exp, act)

    def test_frame(self):
        """When referenced, the Panel.frame property should return a
        string that will draw the panel's frame in the terminal.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}┌────┐'
            f'{term.move(1, 0)}│'
            f'{term.move(1, 5)}│'
            f'{term.move(2, 0)}│'
            f'{term.move(2, 5)}│'
            f'{term.move(3, 0)}│'
            f'{term.move(3, 5)}│'
            f'{term.move(4, 0)}└────┘'
        )

        # Test data and state.
        kwargs = {
            'height': 5,
            'width': 6,
            'term': term,
            'frame_type': 'light',
        }
        panel = p.Panel(**kwargs)

        # Run test.
        act = panel.frame

        # Determine test result.
        self.assertEqual(exp, act)

    def test_frame_with_bg(self):
        """When referenced, the Panel.frame property should return a
        string that will draw the panel's frame in the terminal. If
        there is a background color, the frame should have that color.
        """
        # Expected values.
        exp = (
            f'{term.on_blue}'
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

        # Test data and state.
        kwargs = {
            'height': 5,
            'width': 6,
            'term': term,
            'bg': 'blue',
            'frame_type': 'light',
        }
        panel = p.Panel(**kwargs)

        # Run test.
        act = panel.frame

        # Determine test result.
        self.assertEqual(exp, act)

    def test_frame_with_bg_and_fg(self):
        """When referenced, the Panel.frame property should return a
        string that will draw the panel's frame in the terminal. If
        there are background and a foreground colors, the frame should
        have those colors.
        """
        # Expected values.
        exp = (
            f'{term.red_on_blue}'
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

        # Test data and state.
        kwargs = {
            'height': 5,
            'width': 6,
            'term': term,
            'bg': 'blue',
            'fg': 'red',
            'frame_type': 'light',
        }
        panel = p.Panel(**kwargs)

        # Run test.
        act = panel.frame

        # Determine test result.
        self.assertEqual(exp, act)

    def test_frame_with_fg(self):
        """When referenced, the Panel.frame property should return a
        string that will draw the panel's frame in the terminal. If
        there is a foreground color, the frame should have that color.
        """
        # Expected values.
        exp = (
            f'{term.blue}'
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

        # Test data and state.
        kwargs = {
            'height': 5,
            'width': 6,
            'term': term,
            'fg': 'blue',
            'frame_type': 'light',
        }
        panel = p.Panel(**kwargs)

        # Run test.
        act = panel.frame

        # Determine test result.
        self.assertEqual(exp, act)

    def test_frame_with_frame_bg(self):
        """When referenced, the Panel.frame property should return a
        string that will draw the panel's frame in the terminal. If
        there is a frame background color, the frame should have that
        color.
        """
        # Expected values.
        exp = (
            f'{term.on_blue}'
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

        # Test data and state.
        kwargs = {
            'height': 5,
            'width': 6,
            'term': term,
            'frame_bg': 'blue',
            'frame_type': 'light',
        }
        panel = p.Panel(**kwargs)

        # Run test.
        act = panel.frame

        # Determine test result.
        self.assertEqual(exp, act)

    def test_frame_with_frame_bg_and_bg(self):
        """When referenced, the Panel.frame property should return a
        string that will draw the panel's frame in the terminal. If
        there is a frame background color and a background color, the
        frame should have the frame background color.
        """
        # Expected values.
        exp = (
            f'{term.on_blue}'
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

        # Test data and state.
        kwargs = {
            'height': 5,
            'width': 6,
            'term': term,
            'bg': 'red',
            'frame_bg': 'blue',
            'frame_type': 'light',
        }
        panel = p.Panel(**kwargs)

        # Run test.
        act = panel.frame

        # Determine test result.
        self.assertEqual(exp, act)

    def test_frame_with_frame_fg(self):
        """When referenced, the Panel.frame property should return a
        string that will draw the panel's frame in the terminal. If
        there is a frame foreground color, the frame should have that
        color.
        """
        # Expected values.
        exp = (
            f'{term.blue}'
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

        # Test data and state.
        kwargs = {
            'height': 5,
            'width': 6,
            'term': term,
            'frame_fg': 'blue',
            'frame_type': 'light',
        }
        panel = p.Panel(**kwargs)

        # Run test.
        act = panel.frame

        # Determine test result.
        self.assertEqual(exp, act)

    def test_frame_with_frame_fg_and_fg(self):
        """When referenced, the Panel.frame property should return a
        string that will draw the panel's frame in the terminal. If
        there is a frame foreground color, the frame should have that
        color. If there is a frame foreground color and a foreground
        color, the frame should have the frame foreground color.
        """
        # Expected values.
        exp = (
            f'{term.blue}'
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

        # Test data and state.
        kwargs = {
            'height': 5,
            'width': 6,
            'term': term,
            'fg': 'red',
            'frame_fg': 'blue',
            'frame_type': 'light',
        }
        panel = p.Panel(**kwargs)

        # Run test.
        act = panel.frame

        # Determine test result.
        self.assertEqual(exp, act)


class TitleTestCase(TerminalTestCase):
    def test___init__optional_parameters(self):
        """Given any parameters, a Title should return an
        object with the expected attributes set.
        """
        # Expected values.
        exp = {
            **kwargs_title_opt_set,
            **kwargs_frame_opt_set,
            **kwargs_panel_req,
            **kwargs_panel_opt_set,
        }

        # Run test.
        panel = p.Title(**exp)

        # Gather actuals.
        act = {key: getattr(panel, key) for key in exp}

        # Determine test results.
        self.assertDictEqual(exp, act)

    def test___init__required_parameters(self):
        """Given only the required parameters, a Title should
        return an object with the expected attributes set.
        """
        # Expected values.
        exp_req = kwargs_panel_req
        exp_opt = {
            **kwargs_title_opt_default,
            **kwargs_frame_opt_default,
            **kwargs_panel_opt_default
        }

        # Run test.
        panel = p.Title(**exp_req)

        # Gather actuals.
        act_req = {key: getattr(panel, key) for key in exp_req}
        act_opt = {key: getattr(panel, key) for key in exp_opt}

        # Determine test results.
        self.assertDictEqual(exp_req, act_req)
        self.assertDictEqual(exp_opt, act_opt)

    def test___init__footer_frame_no_frame_type(self):
        """If the footer_frame attribute is set without setting the
        frame_type attribute, the `Title` object should raise a
        `panel.NoFrameTypeForFrameError`.
        """
        # Expected values.
        exp_ex = p.NoFrameTypeForFrameError
        exp_msg = 'You must set frame_type if you set footer_frame.'

        # Test data and state.
        kwargs = {
            'footer_text': 'spam',
            'footer_frame': True,
            'height': 7,
            'width': 10,
            'term': term,
        }

        # Run test and determine test results.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            panel = p.Title(**kwargs)

    def test___init__title_frame_no_frame_type(self):
        """If the title_frame attribute is set without setting the
        title_type attribute, the `Title` object should raise a
        `panel.NoFrameTypeForFrameError`.
        """
        # Expected values.
        exp_ex = p.NoFrameTypeForFrameError
        exp_msg = 'You must set frame_type if you set title_frame.'

        # Test data and state.
        kwargs = {
            'title_text': 'spam',
            'title_frame': True,
            'height': 7,
            'width': 10,
            'term': term,
        }

        # Run test and determine test results.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            panel = p.Title(**kwargs)

    def test___str__(self):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen.
        """
        # Expected values.
        exp = (
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(0, 0)}      '
            f'{term.move(0, 0)}spam'
        )

        # Test data and state.
        kwargs = {
            'title_text': 'spam',
            'height': 5,
            'width': 6,
            'term': term,
        }
        panel = p.Title(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_bg(self):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If the background
        color is set, the title should be that color.
        """
        # Expected values.
        exp = (
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

        # Test data and state.
        kwargs = {
            'title_text': 'spam',
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

    def test___str__with_fg(self):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If the foreground
        color is set, the title should be that color.
        """
        # Expected values.
        exp = (
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

        # Test data and state.
        kwargs = {
            'title_text': 'spam',
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

    def test___str__with_footer(self):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If there is a
        footer, it appears on the bottom of the panel.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(4, 0)}spam'
        )

        # Test data and state.
        kwargs = {
            'footer_text': 'spam',
            'height': 5,
            'width': 6,
            'term': term,
        }
        panel = p.Title(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_footer_align_center(self):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If there is a
        footer, it appears on the bottom of the panel. If there the
        footer align is center, the footer is center of the bottom line
        of the panel.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}          '
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(4, 0)}          '
            f'{term.move(4, 3)}spam'
        )

        # Test data and state.
        kwargs = {
            'footer_text': 'spam',
            'footer_align': 'center',
            'height': 5,
            'width': 10,
            'term': term,
        }
        panel = p.Title(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_footer_align_right(self):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If there is a
        footer, it appears on the bottom of the panel. If there the
        footer align is right, the footer on the right of the bottom
        line of the panel.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}          '
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(4, 0)}          '
            f'{term.move(4, 6)}spam'
        )

        # Test data and state.
        kwargs = {
            'footer_text': 'spam',
            'footer_align': 'right',
            'height': 5,
            'width': 10,
            'term': term,
        }
        panel = p.Title(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_footer_frame(self):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If there is a
        footer, it appears on the bottom of the panel. If there is a
        footer frame, the frame is capped on either side of the footer.
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
            f'{term.move(6, 1)}┤spam├'
        )

        # Test data and state.
        kwargs = {
            'footer_text': 'spam',
            'footer_frame': True,
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

    def test___str__with_frame(self):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If the panel
        has a frame, the title should be on the top line of the frame,
        indented to match left margin of the contents.
        """
        # Expected values.
        exp = (
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

        # Test data and state.
        kwargs = {
            'title_text': 'spam',
            'height': 5,
            'width': 10,
            'term': term,
            'frame_type': 'light',
        }
        panel = p.Title(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_frame_and_frame_bg_and_title_frame(self):
        """When converted to a string, a `Title` object returns a
        string that will draw the panel. If the panel has a frame,
        the title should be on the top line of the frame, indented
        to match left margin of the contents. If the frame has a
        color, the frame should be that color. If the title has a
        frame, the frame should be capped on either side ot the title,
        and the cap should be the same color as the frame.
        """
        # Expected values.
        exp = (
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

        # Test data and state.
        kwargs = {
            'title_text': 'spam',
            'title_frame': True,
            'frame_type': 'light',
            'frame_fg': 'red',
            'frame_bg': 'blue',
            'height': 5,
            'width': 10,
            'term': term,
        }
        panel = p.Title(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_frame_and_overflowing_title(self):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If the panel
        has a frame, the title should be on the top line of the frame,
        indented to match left margin of the contents. If the title
        is longer than the available space, the title is truncated and
        the overflow indicator is added.
        """
        # Expected values.
        exp = (
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

        # Test data and state.
        kwargs = {
            'title_text': 'spameggsbacon',
            'height': 5,
            'width': 10,
            'term': term,
            'frame_type': 'light',
        }
        panel = p.Title(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

    def test___str__with_overflowing_footer(self):
        """When converted to a string, a Title object returns a
        string that will draw the entire splash screen. If there is a
        footer, it appears on the bottom of the panel. If the footer
        is longer than the available space, the footer is truncated and
        the overflow indicator is added.
        """
        # Expected values.
        exp = (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(4, 0)}spa[▸]'
        )

        # Test data and state.
        kwargs = {
            'footer_text': 'spameggs',
            'height': 5,
            'width': 6,
            'term': term,
        }
        panel = p.Title(**kwargs)

        # Run test.
        act = str(panel)

        # Determine test result.
        self.assertEqual(exp, act)

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
