"""
test_log
~~~~~~~~

Unit tests for the `thurible.log` module.
"""
from collections import deque

from thurible import log


# Test case.
def test__init_default_attrs(
    content_attr_defaults,
    frame_attr_defaults,
    panel_attr_defaults,
    title_attr_defaults
):
    """Given only the required parameters, a `log.Log` panel should
    return an object with the expected attributes set.
    """
    dq = deque()
    maxlen = 50
    panel = log.Log(content=dq, maxlen=maxlen)
    assert panel.content == dq
    assert panel.maxlen == maxlen
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


def test__init_optional_attrs(
    content_attr_set,
    frame_attr_set,
    panel_attr_set,
    title_attr_set
):
    """Given any parameters, a `log.Log` panel should return an
    object with the expected attributes set.
    """
    dq = deque(['spam', 'eggs', 'bacon',])
    maxlen = 100
    panel = log.Log(
        content=dq,
        maxlen=maxlen,
        **content_attr_set,
        **title_attr_set,
        **frame_attr_set,
        **panel_attr_set
    )
    assert panel.content == dq
    assert panel.maxlen == maxlen
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
    """When converted to a string, a `log.Log` panel returns a
    string that will draw the entire splash screen.
    """
    panel = log.Log(content=('spam', 'eggs',), height=5, width=6)
    assert str(panel) == (
        f'{term.move(0, 0)}      '
        f'{term.move(1, 0)}      '
        f'{term.move(2, 0)}      '
        f'{term.move(3, 0)}      '
        f'{term.move(4, 0)}      '
        f'{term.move(0, 0)}eggs'
        f'{term.move(1, 0)}spam'
    )


def test_as_str_height_overflow(term):
    """When converted to a string, a `log.Log` panel returns a
    string that will draw the entire splash screen. If there are
    more lines of content than can fit in the panel, the panel
    only displays the top portion of the content that fits in the
    panel.
    """
    panel = log.Log(
        content=('spam', 'eggs', 'bacon', 'ham', 'beans', 'toast'),
        height=5,
        width=6
    )
    assert str(panel) == (
        f'{term.move(0, 0)}      '
        f'{term.move(1, 0)}      '
        f'{term.move(2, 0)}      '
        f'{term.move(3, 0)}      '
        f'{term.move(4, 0)}      '
        f'{term.move(0, 0)}toast'
        f'{term.move(1, 0)}beans'
        f'{term.move(2, 0)}ham'
        f'{term.move(3, 0)}bacon'
        f'{term.move(4, 0)}eggs'
    )


def test_as_str_maxlen_overflow(term):
    """When converted to a string, a `log.Log` panel returns a
    string that will draw the entire splash screen. If there are
    more lines of content than the maximum length of the log, the
    log should drop the overflowing lines.
    """
    panel = log.Log(
        content=('spam', 'eggs', 'bacon', 'ham', 'beans', 'toast'),
        maxlen=3,
        height=5,
        width=6
    )
    assert str(panel) == (
        f'{term.move(0, 0)}      '
        f'{term.move(1, 0)}      '
        f'{term.move(2, 0)}      '
        f'{term.move(3, 0)}      '
        f'{term.move(4, 0)}      '
        f'{term.move(0, 0)}toast'
        f'{term.move(1, 0)}beans'
        f'{term.move(2, 0)}ham'
    )


def test_as_str_width_overflow(term):
    """When converted to a string, a `log.Log` panel returns a
    string that will draw the entire splash screen. If any of
    the lines of content are too long for the panel, they are
    wrapped to the next line.
    """
    panel = log.Log(
        content=('spam eggs', 'bacon ham'),
        height=5,
        width=6
    )
    assert str(panel) == (
        f'{term.move(0, 0)}      '
        f'{term.move(1, 0)}      '
        f'{term.move(2, 0)}      '
        f'{term.move(3, 0)}      '
        f'{term.move(4, 0)}      '
        f'{term.move(0, 0)}bacon'
        f'{term.move(1, 0)}ham'
        f'{term.move(2, 0)}spam'
        f'{term.move(3, 0)}eggs'
    )


def test_update(term):
    """Given an Update message with a string, Log.update() should
    add that string to the top of the log display.
    """
    panel = log.Log(
        content=('spam', 'eggs',),
        height=5,
        width=6
    )
    panel.update(log.Update('bacon'))
    assert str(panel) == (
        f'{term.move(0, 0)}      '
        f'{term.move(1, 0)}      '
        f'{term.move(2, 0)}      '
        f'{term.move(3, 0)}      '
        f'{term.move(4, 0)}      '
        f'{term.move(0, 0)}bacon'
        f'{term.move(1, 0)}eggs'
        f'{term.move(2, 0)}spam'
    )


def test_update_overflows_maxlen(term):
    """Given an Update message with a string, Log.update() should
    add that string to the top of the log display. If the number of
    lines becomes longer than the maximum length of the log, the
    overflowing lines should be dropped.
    """
    panel = log.Log(
        content=('spam', 'eggs',),
        maxlen=2,
        height=5,
        width=6
    )
    panel.update(log.Update('bacon'))
    assert str(panel) == (
        f'{term.move(0, 0)}      '
        f'{term.move(1, 0)}      '
        f'{term.move(2, 0)}      '
        f'{term.move(3, 0)}      '
        f'{term.move(4, 0)}      '
        f'{term.move(0, 0)}bacon'
        f'{term.move(1, 0)}eggs'
    )
