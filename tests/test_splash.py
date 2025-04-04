"""
test_splash
~~~~~~~~~~~

Unit tests for the `thurible.splash` module.
"""
import pytest as pt

from thurible import splash as s


# Test case.
class TestSplash:
    def test__init_default(
        self, content_attr_defaults,
        frame_attr_defaults,
        panel_attr_defaults,
        title_attr_defaults
    ):
        panel = s.Splash()
        assert panel.content == ''
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
        self, content_attr_set,
        frame_attr_set,
        panel_attr_set,
        title_attr_set
    ):
        """Given any parameters, a TitlePanel should return an
        object with the expected attributes set.
        """
        panel = s.Splash(
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
        """When converted to a string, a TitlePanel object returns a
        string that will draw the entire splash screen.
        """
        panel = s.Splash(
            content=(
                '┌┐\n'
                '└┐\n'
                '└┘'
            ),
            height=5,
            width=6
        )
        assert str(panel) == (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(1, 2)}┌┐'
            f'{term.move(2, 2)}└┐'
            f'{term.move(3, 2)}└┘'
        )

    def test_as_str_with_content_align_h_left(self, term):
        """When converted to a string, a TitlePanel object returns
        a string that will draw the entire splash screen. If the
        horizontal content align is set to left, the text of the
        content should be left aligned within the panel.
        """
        panel = s.Splash(
            content=(
                '┌┐\n'
                '└┐\n'
                '└┘'
            ),
            height=5,
            width=6,
            content_align_h='left'
        )
        assert str(panel) == (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(1, 0)}┌┐'
            f'{term.move(2, 0)}└┐'
            f'{term.move(3, 0)}└┘'
        )

    def test___str__with_content_align_h_right(self, term):
        """When converted to a string, a TitlePanel object returns
        a string that will draw the entire splash screen. If the
        horizontal content align is set to right, the text of the
        content should be right aligned within the panel.
        """
        panel = s.Splash(
            content=(
                '┌┐\n'
                '└┐\n'
                '└┘'
            ),
            height=5,
            width=6,
            content_align_h='right'
        )
        assert str(panel) == (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(1, 4)}┌┐'
            f'{term.move(2, 4)}└┐'
            f'{term.move(3, 4)}└┘'
        )

    def test___str__with_content_align_v_bottom(self, term):
        """When converted to a string, a TitlePanel object returns
        a string that will draw the entire splash screen. If the
        vertical content align is set to bottom, the text of the
        content should be bottom aligned within the panel.
        """
        panel = s.Splash(
            content=(
                '┌┐\n'
                '└┐\n'
                '└┘'
            ),
            height=5,
            width=6,
            content_align_v='bottom'
        )
        assert str(panel) == (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(2, 2)}┌┐'
            f'{term.move(3, 2)}└┐'
            f'{term.move(4, 2)}└┘'
        )

    def test___str__with_content_align_v_top(self, term):
        """When converted to a string, a TitlePanel object returns
        a string that will draw the entire splash screen. If the
        vertical content align is set to top, the text of the
        content should be top aligned within the panel.
        """
        panel = s.Splash(
            content=(
                '┌┐\n'
                '└┐\n'
                '└┘'
            ),
            height=5,
            width=6,
            content_align_v='top'
        )
        assert str(panel) == (
            f'{term.move(0, 0)}      '
            f'{term.move(1, 0)}      '
            f'{term.move(2, 0)}      '
            f'{term.move(3, 0)}      '
            f'{term.move(4, 0)}      '
            f'{term.move(0, 2)}┌┐'
            f'{term.move(1, 2)}└┐'
            f'{term.move(2, 2)}└┘'
        )
