"""
test_text
~~~~~~~~~

Unit tests for the termui.text module.
"""
import pytest as pt

from thurible import text


# Test case.
class TestText:
    def test__init_default(
        self, content_attr_defaults_menu,
        frame_attr_defaults,
        panel_attr_defaults,
        title_attr_defaults
    ):
        """Given only the required parameters, a TitlePanel should
        return an object with the expected attributes set.
        """
        panel = text.Text()
        assert panel.content == ''
        assert {
            k: getattr(panel, k) for k in content_attr_defaults_menu
        } == content_attr_defaults_menu
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
        self, content_attr_set,
        frame_attr_set,
        panel_attr_set,
        title_attr_set
    ):
        """Given any parameters, a TitlePanel should return an
        object with the expected attributes set.
        """
        panel = text.Text(
            content='bacon',
            **content_attr_set,
            **title_attr_set,
            **frame_attr_set,
            **panel_attr_set
        )
        assert panel.content == 'bacon'
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

    def test_as_str(self, term):
        """When converted to a string, a Text object returns a string
        that will draw the text.
        """
        panel = text.Text(
            content='spam',
            height=5,
            width=10
        )
        assert str(panel) == (
            f'{term.move(0, 0)}          '
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(4, 0)}          '
            f'{term.move(0, 0)}spam'
        )

    def test_as_str_with_bg_and_fg(self, term):
        """When converted to a string, a Text object returns a string
        that will draw the text. If foreground and background colors
        are set, the contents should be those colors.
        """
        panel = text.Text(
            content='spam',
            height=5,
            width=10,
            bg='blue',
            fg='red'
        )
        assert str(panel) == (
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

    def test_as_str_with_bottom_overflow(self, term):
        """When converted to a string, a Text object returns a string
        that will draw the text. If the text overflows the bottom of
        the display, there should be an indicator showing there is
        overflow.
        """
        panel = text.Text(
            content=(
                'spam eggs '
                'eggs spam '
                'spam eggs '
                'eggs spam '
                'spam eggs '
                'eggs spam '
            ),
            height=5,
            width=10
        )
        assert str(panel) == (
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

    def test_as_str_with_bottom_overflow_and_bg_and_fg(self, term):
        """When converted to a string, a Text object returns a string
        that will draw the text. If the text overflows the bottom of
        the display, there should be an indicator showing there is
        overflow. If there are foreground and background colors set,
        the overflow indicator and the contents should be those colors.
        """
        panel = text.Text(
            content=(
                'spam eggs '
                'eggs spam '
                'spam eggs '
                'eggs spam '
                'spam eggs '
                'eggs spam '
            ),
            height=5,
            width=10,
            bg='blue',
            fg='red'
        )
        assert str(panel) == (
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

    def test_action_down(self, KEY_DOWN, term):
        """When a down arrow is received, Text.action() scrolls down
        in the text.
        """
        panel = text.Text(
            content=(
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
            height=5,
            width=10
        )
        panel._overflow_bottom = True
        panel._stop = 4
        assert panel.action(KEY_DOWN) == ('', (
            f'{term.move(0, 0)}          '
            f'{term.move(0, 3)}[▲]'
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(1, 0)}2pam eggs'
            f'{term.move(2, 0)}3pam eggs'
            f'{term.move(3, 0)}4pam eggs'
        ))

    def test_action_down_cannot_scroll_past_end(self, KEY_DOWN, term):
        """When a down arrow is received, Text.action() scrolls down
        in the text. If already at the bottom of the text, Text.action()
        cannot scroll any farther.
        """
        panel = text.Text(
            content=(
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
            height=5,
            width=10
        )
        panel._overflow_bottom = False
        panel._overflow_top = True
        panel._start = 6
        panel._stop = 10
        assert panel.action(KEY_DOWN) == ('', (
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(4, 0)}          '
            f'{term.move(1, 0)}6pam eggs'
            f'{term.move(2, 0)}7pam eggs'
            f'{term.move(3, 0)}8pam eggs'
            f'{term.move(4, 0)}9pam eggs'
        ))

    def test_action_down_text_smaller_than_screen(self, KEY_DOWN, term):
        """When a down arrow is received, Text.action() scrolls down
        in the text. If the text is too small to scroll, no update is
        returned.
        """
        panel = text.Text(
            content=(
                '0pam eggs '
                '1pam eggs '
            ),
            height=5,
            width=10
        )
        panel._start = 0
        panel._stop = 4
        assert panel.action(KEY_DOWN) == ('', '')

    def test_action_down_reach_near_bottom(self, KEY_DOWN, term):
        """When a down arrow is received, Text.action() scrolls down
        in the text. If the bottom of the text is reached, the bottom
        overflow indicator should not be shown.
        """
        panel = text.Text(
            content=(
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
            height=5,
            width=10
        )
        panel._overflow_bottom = True
        panel._overflow_top = True
        panel._start = 5
        panel._stop = 8
        assert panel.action(KEY_DOWN) == ('', (
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

    def test_action_end(self, KEY_END, term):
        """When a end is received, Text.action() scrolls down
        to the end of the text.
        """
        panel = text.Text(
            content=(
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
            height=5,
            width=10
        )
        panel._overflow_bottom = True
        panel._stop = 4
        assert panel.action(KEY_END) == ('', (
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

    def test_action_home(self, KEY_HOME, term):
        """When a home is received, Text.action() scrolls up
        to the top of the text.
        """
        panel = text.Text(
            content=(
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
            height=5,
            width=10
        )
        panel._overflow_bottom = False
        panel._overflow_top = True
        panel._start = 6
        panel._stop = 10
        assert panel.action(KEY_HOME) == ('', (
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

    def test_action_page_down(self, KEY_PGDOWN, term):
        """When a page down is received, Text.action() scrolls down
        a page in the text.
        """
        panel = text.Text(
            content=(
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
            height=5,
            width=10
        )
        panel._overflow_bottom = True
        panel._stop = 4
        assert panel.action(KEY_PGDOWN) == ('', (
            f'{term.move(0, 0)}          '
            f'{term.move(0, 3)}[▲]'
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(1, 0)}4pam eggs'
            f'{term.move(2, 0)}5pam eggs'
            f'{term.move(3, 0)}6pam eggs'
        ))

    def test_action_page_up(self, KEY_PGUP, term):
        """When a page up is received, Text.action() scrolls up
        a page in the text.
        """
        panel = text.Text(
            content=(
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
            height=5,
            width=10
        )
        panel._overflow_bottom = False
        panel._overflow_top = True
        panel._start = 6
        panel._stop = 10
        assert panel.action(KEY_PGUP) == ('', (
            f'{term.move(4, 0)}          '
            f'{term.move(4, 3)}[▼]'
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(1, 0)}3pam eggs'
            f'{term.move(2, 0)}4pam eggs'
            f'{term.move(3, 0)}5pam eggs'
        ))

    def test_action_unknown_key(self, KEY_X, term):
        """When an unknown key is received, its string value is returned
        as data.
        """
        panel = text.Text(
            content=(
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
            height=5,
            width=10
        )
        panel._overflow_bottom = True
        panel._overflow_top = False
        panel._start = 0
        panel._stop = 4
        assert panel.action(KEY_X) == ('x', '')

    def test_action_up(self, KEY_UP, term):
        """When a up arrow is received, Text.action() scrolls up
        in the text.
        """
        panel = text.Text(
            content=(
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
            height=5,
            width=10
        )
        panel._overflow_bottom = False
        panel._overflow_top = True
        panel._start = 6
        panel._stop = 10
        assert panel.action(KEY_UP) == ('', (
            f'{term.move(4, 0)}          '
            f'{term.move(4, 3)}[▼]'
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(1, 0)}5pam eggs'
            f'{term.move(2, 0)}6pam eggs'
            f'{term.move(3, 0)}7pam eggs'
        ))

    def test_action_up_cannot_scroll_past_top(self, KEY_UP, term):
        """When a up arrow is received, Text.action() scrolls up
        in the text. If already at the bottom of the text, Text.action()
        cannot scroll any farther.
        """
        panel = text.Text(
            content=(
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
            height=5,
            width=10
        )
        panel._overflow_bottom = True
        panel._overflow_top = False
        panel._start = 0
        panel._stop = 4
        assert panel.action(KEY_UP) == ('', (
            f'{term.move(0, 0)}          '
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(0, 0)}0pam eggs'
            f'{term.move(1, 0)}1pam eggs'
            f'{term.move(2, 0)}2pam eggs'
            f'{term.move(3, 0)}3pam eggs'
        ))

    def test_action_up_reach_near_top(self, KEY_UP, term):
        """When a up arrow is received, Text.action() scrolls up
        in the text. If the top of the text is reaches, the top
        overflow indicator should not be shown.
        """
        panel = text.Text(
            content=(
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
            height=5,
            width=10
        )
        panel._overflow_bottom = True
        panel._overflow_top = True
        panel._start = 2
        panel._stop = 5
        assert panel.action(KEY_UP) == ('', (
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

    def test_action_up_text_smaller_than_screen(self, KEY_UP, term):
        """When a up arrow is received, Text.action() scrolls up
        in the text. If the text is too small to scroll, no update is
        returned.
        """
        panel = text.Text(
            content=(
                '0pam eggs '
                '1pam eggs '
            ),
            height=5,
            width=10
        )
        panel._start = 0
        panel._stop = 4
        assert panel.action(KEY_UP) == ('', '')
