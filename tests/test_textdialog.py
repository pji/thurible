"""
test_textdialog
~~~~~~~~~~~~~~~

Unit tests for the `thurible.textdialog` module.
"""
import pytest as pt

from thurible import textdialog


# Test class.
class TestTextDialog:
    def test__init_default(
        self, content_attr_defaults,
        frame_attr_defaults,
        panel_attr_defaults,
        title_attr_defaults
    ):
        """Given only the required parameters, a `TextDialog` should
        return an object with the expected attributes set.
        """
        panel = textdialog.TextDialog(
            message_text='spam'
        )
        assert panel.message_text == 'spam'
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
        """Given only the required parameters, a `TextDialog` should
        return an object with the expected attributes set.
        """
        panel = textdialog.TextDialog(
            message_text='bacon',
            **content_attr_set,
            **title_attr_set,
            **frame_attr_set,
            **panel_attr_set
        )
        assert panel.message_text == 'bacon'
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
        """When converted to a string, a `TextDialog` object returns a
        string that will draw the dialog.
        """
        panel = textdialog.TextDialog(
            message_text='spam',
            height=5,
            width=10
        )
        assert str(panel) == (
            f'{term.move(0, 0)}          '
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(4, 0)}          '
            f'{term.move(2, 0)}spam'
            f'{term.move(4, 0)}> '
            f'{term.reverse}'
            f'{term.move(4, 2)} '
            f'{term.normal}'
        )

    def test_as_str_message_wraps(self, term):
        """When converted to a string, a `TextDialog` object returns a
        string that will draw the dialog. If the message is longer than
        the width of the Dialog, the message text wraps to the next line.
        """
        panel = textdialog.TextDialog(
            message_text='spam eggs bacon',
            height=5,
            width=10
        )
        assert str(panel) == (
            f'{term.move(0, 0)}          '
            f'{term.move(1, 0)}          '
            f'{term.move(2, 0)}          '
            f'{term.move(3, 0)}          '
            f'{term.move(4, 0)}          '
            f'{term.move(1, 0)}spam eggs'
            f'{term.move(2, 0)}bacon'
            f'{term.move(4, 0)}> '
            f'{term.reverse}'
            f'{term.move(4, 2)} '
            f'{term.normal}'
        )

    def test_action_backspace(self, KEY_BACKSPACE, term):
        """When a backspace is received, `TextDialog.action()` should
        delete the previous character.
        """
        panel = textdialog.TextDialog(
            message_text='spam',
            height=5,
            width=10
        )
        panel.value = 'ss'
        panel._selected = 2
        assert panel.action(KEY_BACKSPACE) == ('', (
            f'{term.move(4, 2)}s       '
            f'{term.reverse}'
            f'{term.move(4, 3)} '
            f'{term.normal}'
        ))

    def test_action_delete(self, KEY_DELETE, term):
        """When a delete is received, `TextDialog.action()` should
        delete the selected character.
        """
        panel = textdialog.TextDialog(
            message_text='spam',
            height=5,
            width=10
        )
        panel.value = 'ham'
        panel._selected = 0
        assert panel.action(KEY_DELETE) == ('', (
            f'{term.move(4, 2)}am      '
            f'{term.reverse}'
            f'{term.move(4, 2)}a'
            f'{term.normal}'
        ))

    def test_action_end(self, KEY_END, term):
        """When an end is received, `TextDialog.action()` should
        move the cursor to the last position.
        """
        panel = textdialog.TextDialog(
            message_text='spam',
            height=5,
            width=10
        )
        panel.value = 'ss'
        panel._selected = 0
        assert panel.action(KEY_END) == ('', (
            f'{term.move(4, 2)}ss      '
            f'{term.reverse}'
            f'{term.move(4, 4)} '
            f'{term.normal}'
        ))

    def test_action_enter(self, KEY_ENTER, term):
        """When an enter is received, `TextDialog.action()` should
        return the previously entered text as data.
        """
        panel = textdialog.TextDialog(
            message_text='spam',
            height=5,
            width=10
        )
        panel.value = 'eggs'
        assert panel.action(KEY_ENTER) == ('eggs', '')

    def test_action_home(self, KEY_HOME, term):
        """When a home is received, `TextDialog.action()` should
        move the cursor to the first character.
        """
        panel = textdialog.TextDialog(
            message_text='spam',
            height=5,
            width=10
        )
        panel.value = 'ss'
        panel._selected = 2
        assert panel.action(KEY_HOME) == ('', (
            f'{term.move(4, 2)}ss      '
            f'{term.reverse}'
            f'{term.move(4, 2)}s'
            f'{term.normal}'
        ))

    def test_action_left(self, KEY_LEFT, term):
        """When a home is received, `TextDialog.action()` should
        move the cursor to the first character.
        """
        panel = textdialog.TextDialog(
            message_text='spam',
            height=5,
            width=10
        )
        panel.value = 'ss'
        panel._selected = 2
        assert panel.action(KEY_LEFT) == ('', (
            f'{term.move(4, 2)}ss      '
            f'{term.reverse}'
            f'{term.move(4, 3)}s'
            f'{term.normal}'
        ))

    def test_action_left_cannot_go_past_home(self, KEY_LEFT, term):
        """When a left arrow is received, `TextDialog.action()` should
        move the cursor to the previous character. If at the left-most
        character, the cursor cannot move to a previous character.
        """
        panel = textdialog.TextDialog(
            message_text='spam',
            height=5,
            width=10
        )
        panel.value = 'ss'
        panel._selected = 0
        assert panel.action(KEY_LEFT) == ('', (
            f'{term.move(4, 2)}ss      '
            f'{term.reverse}'
            f'{term.move(4, 2)}s'
            f'{term.normal}'
        ))

    def test_action_not_a_keystroke(self, term):
        """When something other than a keystroke is received,
        `TextDialog.action()` should throw a ValueError exception.
        """
        panel = textdialog.TextDialog(
            message_text='spam',
            height=5,
            width=10
        )
        with pt.raises(ValueError) as ex:
            panel.action('\x00')
            assert str(ex) == 'Can only accept Keystrokes. Received: str.'

    def test_action_right(self, KEY_RIGHT, term):
        """When a right arrow is received, `TextDialog.action()` should
        move the cursor to the next character.
        """
        panel = textdialog.TextDialog(
            message_text='spam',
            height=5,
            width=10
        )
        panel.value = 'ss'
        panel._selected = 0
        assert panel.action(KEY_RIGHT) == ('', (
            f'{term.move(4, 2)}ss      '
            f'{term.reverse}'
            f'{term.move(4, 3)}s'
            f'{term.normal}'
        ))

    def test_action_right_arrow_cannot_go_past_end(self, KEY_RIGHT, term):
        """When a right arrow is received, `TextDialog.action()` should
        move the cursor to the next character. If the cursor is in the
        right-most position, the cursor cannot move to the right.
        """
        panel = textdialog.TextDialog(
            message_text='spam',
            height=5,
            width=10
        )
        panel.value = 'ss'
        panel._selected = 2
        assert panel.action(KEY_RIGHT) == ('', (
            f'{term.move(4, 2)}ss      '
            f'{term.reverse}'
            f'{term.move(4, 4)} '
            f'{term.normal}'
        ))

    def test_action_s(self, KEY_S, term):
        """When an `s` is received, `TextDialog.action()` should update
        the text entry area to include the `s` and move the cursor one
        column to the right.
        """
        panel = textdialog.TextDialog(
            message_text='spam',
            height=5,
            width=10
        )
        panel._selected = 0
        assert panel.action(KEY_S) == ('', (
            f'{term.move(4, 2)}s       '
            f'{term.reverse}'
            f'{term.move(4, 3)} '
            f'{term.normal}'
        ))

    def test_action_s_with_value(self, KEY_S, term):
        """When an `s` is received, `TextDialog.action()` should update
        the text entry area to include the `s` and move the cursor one
        column to the right.
        """
        panel = textdialog.TextDialog(
            message_text='spam',
            height=5,
            width=10
        )
        panel._selected = 1
        panel.value = 's'
        assert panel.action(KEY_S) == ('', (
            f'{term.move(4, 2)}ss      '
            f'{term.reverse}'
            f'{term.move(4, 4)} '
            f'{term.normal}'
        ))

    def test_action_s_with_value_inserting_character(self, KEY_S, term):
        """When an `s` is received, `TextDialog.action()` should update
        the text entry area to include the `s` and move the cursor one
        column to the right. If the cursor has selected a character in
        the value, the typed character is inserted before the selected
        character.
        """
        panel = textdialog.TextDialog(
            message_text='spam',
            height=5,
            width=10
        )
        panel._selected = 1
        panel.value = 'aa'
        assert panel.action(KEY_S) == ('', (
            f'{term.move(4, 2)}asa     '
            f'{term.reverse}'
            f'{term.move(4, 4)}a'
            f'{term.normal}'
        ))

    def test_action_undefined_application_key(self, KEY_F1, term):
        """When an "application" keystroke whose behavior has not been
        defined is received, `TextDialog.action()` should return the
        string value of the keystroke as data.
        """
        panel = textdialog.TextDialog(
            message_text='spam',
            height=5,
            width=10
        )
        panel.value = 'eggs'
        assert panel.action(KEY_F1) == ('\x1bOP', '')

    def test_action_undefined_control_key(self, KEY_BELL, term):
        """When an "application" keystroke whose behavior has not been
        defined is received, `TextDialog.action()` should return the
        string value of the keystroke as data.
        """
        panel = textdialog.TextDialog(
            message_text='spam',
            height=5,
            width=10
        )
        panel.value = 'eggs'
        assert panel.action(KEY_BELL) == ('\x07', '')
