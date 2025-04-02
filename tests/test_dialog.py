"""
test_dialog
~~~~~~~~~~~

Unit tests for the `thurible.dialog` module.
"""
import pytest as pt

from thurible import dialog


# Test cases.
def test_init_defaults(
    content_attr_defaults,
    title_attr_defaults,
    frame_attr_defaults,
    panel_attr_defaults
):
    """Given only the required parameters, a thurible.dialog.Dialog
    should return an object with the expected attributes set.
    """
    text = 'spam'
    d = dialog.Dialog(message_text=text)
    assert d.message_text == text
    assert d.options == dialog.yes_no
    assert {
        k: getattr(d, k) for k in content_attr_defaults
    } == content_attr_defaults
    assert {
        k: getattr(d, k) for k in title_attr_defaults
    } == title_attr_defaults
    assert {
        k: getattr(d, k) for k in frame_attr_defaults
    } == frame_attr_defaults
    assert {
        k: getattr(d, k) for k in panel_attr_defaults
    } == panel_attr_defaults


def test_init_set(
    content_attr_set,
    title_attr_set,
    frame_attr_set,
    panel_attr_set
):
    """Given all parameters, a thurible.dialog.Dialog should
    return an object with the expected attributes set.
    """
    text = 'spam'
    options = [
        dialog.Option('Eggs', 'e'),
        dialog.Option('Bacon', 'b'),
    ]
    d = dialog.Dialog(
        message_text=text,
        options=options,
        **content_attr_set,
        **title_attr_set,
        **frame_attr_set,
        **panel_attr_set
    )
    assert d.message_text == text
    assert d.options == options
    assert {
        k: getattr(d, k) for k in content_attr_set
    } == content_attr_set
    assert {
        k: getattr(d, k) for k in title_attr_set
    } == title_attr_set
    assert {
        k: getattr(d, k) for k in frame_attr_set
    } == frame_attr_set
    assert {
        k: getattr(d, k) for k in panel_attr_set
    } == panel_attr_set


def test_to_str(term):
    """When converted to a string, a Dialog object returns a string
    that will draw the dialog.
    """
    d = dialog.Dialog('spam', height=5, width=10)
    assert str(d) == (
        f'{term.move(0, 0)}          '
        f'{term.move(1, 0)}          '
        f'{term.move(2, 0)}          '
        f'{term.move(3, 0)}          '
        f'{term.move(4, 0)}          '
        f'{term.move(2, 0)}spam'
        f'{term.reverse}'
        f'{term.move(4, 6)}[No]'
        f'{term.normal}'
        f'{term.move(4, 0)}[Yes]'
    )


def test_to_str_wrapping_message(term):
    """When converted to a string, a Dialog object returns a string
    that will draw the dialog. If the message is longer than the
    width of the Dialog, the message text wraps to the next line.
    """
    d = dialog.Dialog('spam eggs bacon', height=5, width=10)
    assert str(d) == (
        f'{term.move(0, 0)}          '
        f'{term.move(1, 0)}          '
        f'{term.move(2, 0)}          '
        f'{term.move(3, 0)}          '
        f'{term.move(4, 0)}          '
        f'{term.move(1, 0)}spam eggs'
        f'{term.move(2, 0)}bacon'
        f'{term.reverse}'
        f'{term.move(4, 6)}[No]'
        f'{term.normal}'
        f'{term.move(4, 0)}[Yes]'
    )


def test_action_enter(KEY_ENTER):
    """When a enter is received, `Dialog.action()` should return
    the name of the option selected.
    """
    d = dialog.Dialog('spam', height=5, width=10)
    assert d.action(KEY_ENTER) == ('No', '')


def test_action_hotkey(term, KEY_Y):
    """When a hot key is received, `Dialog.action()` should move
    the selection to the option assigned to the hot key.
    """
    d = dialog.Dialog('spam', height=5, width=10)
    assert d.action(KEY_Y) == ('', (
        f'{term.move(4, 6)}[No]'
        f'{term.reverse}'
        f'{term.move(4, 0)}[Yes]'
        f'{term.normal}'
    ))


def test_action_left(term, KEY_LEFT):
    """When a left arrow is received, `Dialog.action()` should move
    the selection to the option assigned to the hot key.
    """
    d = dialog.Dialog('spam', height=5, width=10)
    assert d.action(KEY_LEFT) == ('', (
        f'{term.move(4, 6)}[No]'
        f'{term.reverse}'
        f'{term.move(4, 0)}[Yes]'
        f'{term.normal}'
    ))


def test_action_left_at_far_left(term, KEY_LEFT):
    """When a left arrow is received, `Dialog.action()` should move
    the selection to the next option to the left of the current
    selection. If the selection is already at the left-most option,
    the selection should not move.
    """
    d = dialog.Dialog('spam', height=5, width=10)
    d._selected = 0
    assert d.action(KEY_LEFT) == ('', (
        f'{term.move(4, 6)}[No]'
        f'{term.reverse}'
        f'{term.move(4, 0)}[Yes]'
        f'{term.normal}'
    ))


def test_action_right(term, KEY_RIGHT):
    """When a right arrow is received, `Dialog.action()` should
    move the selection to the next option to the left of the
    current selection.
    """
    d = dialog.Dialog('spam', height=5, width=10)
    d._selected = 0
    assert d.action(KEY_RIGHT) == ('', (
        f'{term.reverse}'
        f'{term.move(4, 6)}[No]'
        f'{term.normal}'
        f'{term.move(4, 0)}[Yes]'
    ))


def test_action_right_at_far_right(term, KEY_RIGHT):
    """When a right arrow is received, `Dialog.action()` should
    move the selection to the next option to the left of the
    current selection. If the selection is already at the
    right-most option, the selection should not move.
    """
    d = dialog.Dialog('spam', height=5, width=10)
    d._selected = len(dialog.yes_no) - 1
    assert d.action(KEY_RIGHT) == ('', (
        f'{term.reverse}'
        f'{term.move(4, 6)}[No]'
        f'{term.normal}'
        f'{term.move(4, 0)}[Yes]'
    ))
