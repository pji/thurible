"""
test_menu
~~~~~~~~~

Unit tests for the `thurible.menu` module.
"""
import unittest as ut

import pytest as pt

from thurible import menu


# Fixtures.
@pt.fixture
def menu_options(menu_options_very_long):
    """Common menu options."""
    return menu_options_very_long[:3]


@pt.fixture
def menu_options_long(menu_options_very_long):
    """Long list of common menu options."""
    return menu_options_very_long[:7]


@pt.fixture
def menu_options_very_long():
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


# Test case.
def test__init_attrs_default(
    content_attr_defaults_menu,
    frame_attr_defaults,
    menu_options,
    panel_attr_defaults,
    title_attr_defaults
):
    """Given only the required parameters, a Menu should
    return an object with the expected attributes set.
    """
    m = menu.Menu(options=menu_options)
    assert m.options == menu_options
    assert m.select_bg == ''
    assert m.select_fg == ''
    assert m.option_align_h == 'left'
    assert {
        k: getattr(m, k) for k in content_attr_defaults_menu
    } == content_attr_defaults_menu
    assert {
        k: getattr(m, k) for k in title_attr_defaults
    } == title_attr_defaults
    assert {
        k: getattr(m, k) for k in frame_attr_defaults
    } == frame_attr_defaults
    assert {
        k: getattr(m, k) for k in panel_attr_defaults
    } == panel_attr_defaults


def test__init_attrs_set(
    content_attr_set,
    frame_attr_set,
    menu_options,
    panel_attr_set,
    title_attr_set
):
    """Given any parameters, a Menu should return an
    object with the expected attributes set.
    """
    m = menu.Menu(
        options=menu_options,
        select_bg='red',
        select_fg='blue',
        option_align_h='right',
        **content_attr_set,
        **title_attr_set,
        **frame_attr_set,
        **panel_attr_set
    )
    assert m.options == menu_options
    assert m.select_bg == 'red'
    assert m.select_fg == 'blue'
    assert m.option_align_h == 'right'
    assert {
        k: getattr(m, k) for k in content_attr_set
    } == content_attr_set
    assert {
        k: getattr(m, k) for k in title_attr_set
    } == title_attr_set
    assert {
        k: getattr(m, k) for k in frame_attr_set
    } == frame_attr_set
    assert {
        k: getattr(m, k) for k in panel_attr_set
    } == panel_attr_set


def test_as_str(menu_options, term):
    """When converted to a string, a Menu object returns a string
    that will draw the entire menu.
    """
    m = menu.Menu(options=menu_options, height=5, width=7)
    assert str(m) == (
        f'{term.move(0, 0)}       '
        f'{term.move(1, 0)}       '
        f'{term.move(2, 0)}       '
        f'{term.move(3, 0)}       '
        f'{term.move(4, 0)}       '
        f'{term.reverse}'
        f'{term.move(0, 0)}spam '
        f'{term.normal}'
        f'{term.move(1, 0)}eggs '
        f'{term.move(2, 0)}bacon'
    )


def test_as_str_with_bg_and_fg(menu_options, term):
    """When converted to a string, a Menu object returns a string
    that will draw the entire menu. If foreground or background
    colors are given, the contents of the panel should have those
    colors.
    """
    m = menu.Menu(
        options=menu_options,
        height=5,
        width=7,
        bg='blue',
        fg='red'
    )
    assert str(m) == (
        f'{term.red_on_blue}'
        f'{term.move(0, 0)}       '
        f'{term.move(1, 0)}       '
        f'{term.move(2, 0)}       '
        f'{term.move(3, 0)}       '
        f'{term.move(4, 0)}       '
        f'{term.normal}'
        f'{term.red_on_blue}'
        f'{term.reverse}'
        f'{term.move(0, 0)}spam '
        f'{term.normal}'
        f'{term.red_on_blue}'
        f'{term.move(1, 0)}eggs '
        f'{term.move(2, 0)}bacon'
        f'{term.normal}'
    )


def test_as_str_with_content_and_option_align_h_center(menu_options, term):
    """When converted to a string, a Menu object returns a string
    that will draw the entire menu. If the horizontal content
    alignment is centered, the options should be centered within
    the panel.
    """
    m = menu.Menu(
        options=[*menu_options, menu.Option('ham', 'h')],
        option_align_h='center',
        content_align_h='center',
        height=5,
        width=9
    )
    assert str(m) == (
        f'{term.move(0, 0)}         '
        f'{term.move(1, 0)}         '
        f'{term.move(2, 0)}         '
        f'{term.move(3, 0)}         '
        f'{term.move(4, 0)}         '
        f'{term.reverse}'
        f'{term.move(0, 2)}spam '
        f'{term.normal}'
        f'{term.move(1, 2)}eggs '
        f'{term.move(2, 2)}bacon'
        f'{term.move(3, 2)} ham '
    )


def test_as_str_with_content_and_option_align_h_right(menu_options, term):
    """When converted to a string, a Menu object returns a string
    that will draw the entire menu. If the horizontal content
    alignment is right, the options should be right aligned within
    the panel.
    """
    m = menu.Menu(
        options=[*menu_options, menu.Option('ham', 'h')],
        option_align_h='right',
        content_align_h='right',
        height=5,
        width=9
    )
    assert str(m) == (
        f'{term.move(0, 0)}         '
        f'{term.move(1, 0)}         '
        f'{term.move(2, 0)}         '
        f'{term.move(3, 0)}         '
        f'{term.move(4, 0)}         '
        f'{term.reverse}'
        f'{term.move(0, 4)} spam'
        f'{term.normal}'
        f'{term.move(1, 4)} eggs'
        f'{term.move(2, 4)}bacon'
        f'{term.move(3, 4)}  ham'
    )


def test_as_str_with_content_pad_left(menu_options, term):
    """When converted to a string, a Menu object returns a string
    that will draw the entire menu. If left content padding is set,
    the options will be inset by the amount of padding.
    """
    m = menu.Menu(
        options=menu_options,
        content_pad_left=0.2,
        height=5,
        width=10
    )
    assert str(m) == (
        f'{term.move(0, 0)}          '
        f'{term.move(1, 0)}          '
        f'{term.move(2, 0)}          '
        f'{term.move(3, 0)}          '
        f'{term.move(4, 0)}          '
        f'{term.reverse}'
        f'{term.move(0, 3)}spam '
        f'{term.normal}'
        f'{term.move(1, 3)}eggs '
        f'{term.move(2, 3)}bacon'
    )


def test_as_str_with_content_relative_width_and_align_h_center(
    menu_options, term
):
    """When converted to a string, a Menu object returns a string
    that will draw the entire menu. If left content padding is set,
    the options will be inset by the amount of padding.
    """
    m = menu.Menu(
        options=menu_options,
        option_align_h='right',
        content_align_h='center',
        content_relative_width=0.8,
        height=5,
        width=10
    )
    assert str(m) == (
        f'{term.move(0, 0)}          '
        f'{term.move(1, 0)}          '
        f'{term.move(2, 0)}          '
        f'{term.move(3, 0)}          '
        f'{term.move(4, 0)}          '
        f'{term.reverse}'
        f'{term.move(0, 2)} spam'
        f'{term.normal}'
        f'{term.move(1, 2)} eggs'
        f'{term.move(2, 2)}bacon'
    )


def test_as_str_with_overflow(menu_options_long, term):
    """When converted to a string, a Menu object returns a string
    that will draw the entire menu. If there are too many options
    to fit in the panel, there should be an overflow indicator on
    the bottom line of the panel's content.
    """
    m = menu.Menu(
        options=menu_options_long,
        height=5,
        width=9
    )
    assert str(m) == (
        f'{term.move(0, 0)}         '
        f'{term.move(1, 0)}         '
        f'{term.move(2, 0)}         '
        f'{term.move(3, 0)}         '
        f'{term.move(4, 0)}         '
        f'{term.move(4, 0)}         '
        f'{term.move(4, 3)}[▼]'
        f'{term.reverse}'
        f'{term.move(0, 0)}spam  '
        f'{term.normal}'
        f'{term.move(1, 0)}eggs  '
        f'{term.move(2, 0)}bacon '
        f'{term.move(3, 0)}ham   '
    )


def test_as_str_with_select_bg_and_fg(menu_options, term):
    """When converted to a string, a Menu object returns a string
    that will draw the entire menu. If foreground and background
    colors are set for the selection, the selection should be those
    colors.
    """
    m = menu.Menu(
        options=menu_options,
        select_bg='blue',
        select_fg='red',
        height=5,
        width=7
    )
    assert str(m) == (
        f'{term.move(0, 0)}       '
        f'{term.move(1, 0)}       '
        f'{term.move(2, 0)}       '
        f'{term.move(3, 0)}       '
        f'{term.move(4, 0)}       '
        f'{term.red_on_blue}'
        f'{term.move(0, 0)}spam '
        f'{term.normal}'
        f'{term.move(1, 0)}eggs '
        f'{term.move(2, 0)}bacon'
    )


def test_action_down(KEY_DOWN, menu_options_long, term):
    """When a down arrow is received, Menu.action() selects the
    next option.
    """
    m = menu.Menu(
        options=menu_options_long,
        height=5,
        width=9
    )
    m._overflow_bottom = True
    m._stop = 4
    assert m.action(KEY_DOWN) == ('', (
        f'{term.move(0, 0)}spam  '
        f'{term.reverse}'
        f'{term.move(1, 0)}eggs  '
        f'{term.normal}'
        f'{term.move(2, 0)}bacon '
        f'{term.move(3, 0)}ham   '
    ))


def test_action_down_at_bottom(KEY_DOWN, menu_options_long, term):
    """When a down arrow is received, Menu.action() selects the
    next option. If the selected option is the last option, the
    selection doesn't move.
    """
    m = menu.Menu(
        options=menu_options_long,
        height=5,
        width=9
    )
    m._overflow_top = True
    m._selected = 6
    m._start = 3
    m._stop = 7
    assert m.action(KEY_DOWN) == ('', (
        f'{term.move(1, 0)}ham   '
        f'{term.move(2, 0)}beans '
        f'{term.move(3, 0)}toast '
        f'{term.reverse}'
        f'{term.move(4, 0)}tomato'
        f'{term.normal}'
    ))


def test_action_down_scrolls_to_overflow(KEY_DOWN, menu_options_long, term):
    """When a down arrow is received, Menu.action() selects the
    next option. If the selected option is the last visible
    options and the list of option overflows, the list of options
    should scroll down to see the next option.
    """
    m = menu.Menu(
        options=menu_options_long,
        height=5,
        width=9
    )
    m._overflow_bottom = True
    m._selected = 3
    m._stop = 4
    assert m.action(KEY_DOWN) == ('', (
        f'{term.move(0, 0)}         '
        f'{term.move(0, 3)}[▲]'
        f'{term.move(1, 0)}bacon '
        f'{term.move(2, 0)}ham   '
        f'{term.reverse}'
        f'{term.move(3, 0)}beans '
        f'{term.normal}'
    ))


def test_action_down_scrolls_near_bottom_of_overflow(
    KEY_DOWN, menu_options_long, term
):
    """When a down arrow is received, Menu.action() selects the
    next option. If the selected option is the last visible
    options and the list of option overflows, the list of options
    should scroll down to see the next option. If it scrolls to
    the next to last option, the overflow down marker should be
    replaced with the last option.
    """
    m = menu.Menu(
        options=menu_options_long,
        height=5,
        width=9
    )
    m._overflow_bottom = True
    m._overflow_top = True
    m._selected = 4
    m._start = 2
    m._stop = 5
    assert m.action(KEY_DOWN) == ('', (
        f'{term.move(4, 0)}         '
        f'{term.move(1, 0)}ham   '
        f'{term.move(2, 0)}beans '
        f'{term.reverse}'
        f'{term.move(3, 0)}toast '
        f'{term.normal}'
        f'{term.move(4, 0)}tomato'
    ))


def test_action_down_with_content_pad_left(KEY_DOWN, menu_options_long, term):
    """When a down arrow is received, Menu.action() selects the
    next option.
    """
    m = menu.Menu(
        options=menu_options_long,
        content_pad_left=0.2,
        height=5,
        width=10
    )
    m._overflow_bottom = True
    m._stop = 4
    assert m.action(KEY_DOWN) == ('', (
        f'{term.move(0, 3)}spam  '
        f'{term.reverse}'
        f'{term.move(1, 3)}eggs  '
        f'{term.normal}'
        f'{term.move(2, 3)}bacon '
        f'{term.move(3, 3)}ham   '
    ))


def test_action_end(KEY_END, menu_options_long, term):
    """When an end is received, Menu.action() selects the
    last option and jumps to that section of the menu.
    """
    m = menu.Menu(
        options=menu_options_long,
        height=5,
        width=9
    )
    m._overflow_bottom = True
    m._selected = 2
    m._stop = 4
    assert m.action(KEY_END) == ('', (
        f'{term.move(4, 0)}         '
        f'{term.move(0, 0)}         '
        f'{term.move(0, 3)}[▲]'
        f'{term.move(1, 0)}ham   '
        f'{term.move(2, 0)}beans '
        f'{term.move(3, 0)}toast '
        f'{term.reverse}'
        f'{term.move(4, 0)}tomato'
        f'{term.normal}'
    ))


def test_action_home(KEY_HOME, menu_options_long, term):
    """When a home is received, Menu.action() selects the
    last option and jumps to that section of the menu.
    """
    m = menu.Menu(
        options=menu_options_long,
        height=5,
        width=9
    )
    m._overflow_top = True
    m._selected = 5
    m._start = 3
    m._stop = 7
    assert m.action(KEY_HOME) == ('', (
        f'{term.move(4, 0)}         '
        f'{term.move(4, 3)}[▼]'
        f'{term.move(0, 0)}         '
        f'{term.reverse}'
        f'{term.move(0, 0)}spam  '
        f'{term.normal}'
        f'{term.move(1, 0)}eggs  '
        f'{term.move(2, 0)}bacon '
        f'{term.move(3, 0)}ham   '
    ))


def test_action_hotkey(KEY_E, menu_options_long, term):
    """When a hotkey for an option is received, the selection
    jumps to that option.
    """
    m = menu.Menu(
        options=menu_options_long,
        height=5,
        width=9
    )
    m._overflow_top = True
    m._selected = 5
    m._start = 3
    m._stop = 7
    assert m.action(KEY_E) == ('', (
        f'{term.move(4, 0)}         '
        f'{term.move(4, 3)}[▼]'
        f'{term.move(0, 0)}         '
        f'{term.move(0, 0)}spam  '
        f'{term.reverse}'
        f'{term.move(1, 0)}eggs  '
        f'{term.normal}'
        f'{term.move(2, 0)}bacon '
        f'{term.move(3, 0)}ham   '
    ))


def test_action_hotkey_near_bottom_of_overflow(
    KEY_O, menu_options_long, term
):
    """When a hotkey for an option is received, the selection
    jumps to that option. If it jumps to the next to last option,
    that option should not be hidden by the overflow indicator.
    """
    m = menu.Menu(
        options=menu_options_long,
        height=5,
        width=9
    )
    m._overflow_top = False
    m._overflow_bottom = True
    m._selected = 0
    m._start = 0
    m._stop = 4
    assert m.action(KEY_O) == ('', (
        f'{term.move(4, 0)}         '
        f'{term.move(0, 0)}         '
        f'{term.move(0, 3)}[▲]'
        f'{term.move(1, 0)}ham   '
        f'{term.move(2, 0)}beans '
        f'{term.reverse}'
        f'{term.move(3, 0)}toast '
        f'{term.normal}'
        f'{term.move(4, 0)}tomato'
    ))


def test_action_page_down(KEY_PGDOWN, menu_options_very_long, term):
    """When a page down is received and the menu overflows,
    Menu.action() scrolls down by the height of the display and
    selects the option that is now in the position that was
    selected before the page down.
    """
    m = menu.Menu(
        options=menu_options_very_long,
        height=5,
        width=9
    )
    m._overflow_top = True
    m._overflow_bottom = True
    m._selected = 3
    m._start = 2
    m._stop = 5
    assert m.action(KEY_PGDOWN) == ('', (
        f'{term.move(1, 0)}toast '
        f'{term.reverse}'
        f'{term.move(2, 0)}tomato'
        f'{term.normal}'
        f'{term.move(3, 0)}coffee'
    ))


def test_action_page_down_at_bottom(KEY_PGDOWN, menu_options_very_long, term):
    """When a page down is received and the selection would be
    greater than the number of options in the menu, the selection
    becomes the bottom option.
    """
    m = menu.Menu(
        options=menu_options_very_long,
        height=5,
        width=9
    )
    m._overflow_top = True
    m._overflow_bottom = False
    m._selected = 8
    m._start = 6
    m._stop = 10
    assert m.action(KEY_PGDOWN) == ('', (
        f'{term.move(1, 0)}tomato'
        f'{term.move(2, 0)}coffee'
        f'{term.move(3, 0)}muffin'
        f'{term.reverse}'
        f'{term.move(4, 0)}grits '
        f'{term.normal}'
    ))


def test_action_page_down_from_top(KEY_PGDOWN, menu_options_very_long, term):
    """When a page down is received and the menu overflows,
    Menu.action() scrolls down by the height of the display and
    selects the option that is now in the position that was
    selected before the page down. If that position would now be
    covered by an top overflow indicator, scroll the menu up one
    line to keep the selected option visible.
    """
    m = menu.Menu(
        options=menu_options_very_long,
        height=5,
        width=9
    )
    m._overflow_top = False
    m._overflow_bottom = True
    m._selected = 0
    m._start = 0
    m._stop = 4
    assert m.action(KEY_PGDOWN) == ('', (
        f'{term.move(0, 0)}         '
        f'{term.move(0, 3)}[▲]'
        f'{term.reverse}'
        f'{term.move(1, 0)}beans '
        f'{term.normal}'
        f'{term.move(2, 0)}toast '
        f'{term.move(3, 0)}tomato'
    ))


def test_action_page_up(KEY_PGUP, menu_options_very_long, term):
    """When a page up is received and the menu overflows,
    Menu.action() scrolls up by the height of the display and
    selects the option that is now in the position that was
    selected before the page up.
    """
    m = menu.Menu(
        options=menu_options_very_long,
        height=5,
        width=9
    )
    m._overflow_top = True
    m._overflow_bottom = True
    m._selected = 6
    m._start = 5
    m._stop = 8
    assert m.action(KEY_PGUP) == ('', (
        f'{term.move(1, 0)}bacon '
        f'{term.reverse}'
        f'{term.move(2, 0)}ham   '
        f'{term.normal}'
        f'{term.move(3, 0)}beans '
    ))


def test_action_page_up_at_top(KEY_PGUP, menu_options_very_long, term):
    """When a page up is received and the selection would be
    less than zero, the selection becomes the top option.
    """
    m = menu.Menu(
        options=menu_options_very_long,
        height=5,
        width=9
    )
    m._overflow_top = False
    m._overflow_bottom = True
    m._selected = 1
    m._start = 0
    m._stop = 4
    assert m.action(KEY_PGUP) == ('', (
        f'{term.reverse}'
        f'{term.move(0, 0)}spam  '
        f'{term.normal}'
        f'{term.move(1, 0)}eggs  '
        f'{term.move(2, 0)}bacon '
        f'{term.move(3, 0)}ham   '
    ))


def test_action_page_up_from_bottom(KEY_PGUP, menu_options_very_long, term):
    """When a page up is received and the menu overflows,
    Menu.action() scrolls up by the height of the display and
    selects the option that is now in the position that was
    selected before the page up. If that position would now be
    covered by an top overflow indicator, scroll the menu down
    one line to keep the selected option visible.
    """
    m = menu.Menu(
        options=menu_options_very_long,
        height=5,
        width=9
    )
    m._overflow_top = True
    m._overflow_bottom = False
    m._selected = 9
    m._start = 6
    m._stop = 10
    assert m.action(KEY_PGUP) == ('', (
        f'{term.move(4, 0)}         '
        f'{term.move(4, 3)}[▼]'
        f'{term.move(1, 0)}ham   '
        f'{term.move(2, 0)}beans '
        f'{term.reverse}'
        f'{term.move(3, 0)}toast '
        f'{term.normal}'
    ))


def test_action_enter(KEY_ENTER, menu_options_long, term):
    """When an enter is received, Menu.action() should return
    the name of the currently selected option as data.
    """
    m = menu.Menu(
        options=menu_options_long,
        height=5,
        width=9
    )
    m._overflow_bottom = True
    m._selected = 2
    m._stop = 4
    assert m.action(KEY_ENTER) == ('bacon', '')


def test_action_unknown_key(KEY_X, menu_options_long, term):
    """When an unknown key is received, its string value is returned
    as data.
    """
    m = menu.Menu(
        options=menu_options_long,
        height=5,
        width=9
    )
    m._overflow_bottom = True
    m._overflow_top = False
    m._start = 0
    m._stop = 4
    assert m.action(KEY_X) == ('x', '')


def test_action_up(KEY_UP, menu_options_long, term):
    """When an up arrow is received, Menu.action() selects the
    previous option.
    """
    m = menu.Menu(
        options=menu_options_long,
        height=5,
        width=9
    )
    m._overflow_bottom = True
    m._selected = 2
    m._stop = 4
    assert m.action(KEY_UP) == ('', (
        f'{term.move(0, 0)}spam  '
        f'{term.reverse}'
        f'{term.move(1, 0)}eggs  '
        f'{term.normal}'
        f'{term.move(2, 0)}bacon '
        f'{term.move(3, 0)}ham   '
    ))


def test_action_up_at_bottom(KEY_UP, menu_options_long, term):
    """When an up arrow is received, Menu.action() selects the
    previous option. If this was done at the botom of the menu
    and the next option is visible, the menu does not scroll up.
    """
    m = menu.Menu(
        options=menu_options_long,
        height=5,
        width=9
    )
    m._overflow_bottom = False
    m._overflow_top = True
    m._selected = 6
    m._start = 3
    m._stop = 7
    assert m.action(KEY_UP) == ('', (
        f'{term.move(1, 0)}ham   '
        f'{term.move(2, 0)}beans '
        f'{term.reverse}'
        f'{term.move(3, 0)}toast '
        f'{term.normal}'
        f'{term.move(4, 0)}tomato'
    ))


def test_action_up_at_top(KEY_UP, menu_options_long, term):
    """When an up arrow is received, Menu.action() selects the
    previous option. If the selected option is the top option,
    the selection shouldn't move.
    """
    m = menu.Menu(
        options=menu_options_long,
        height=5,
        width=9
    )
    m._overflow_bottom = True
    m._selected = 0
    m._stop = 4
    assert m.action(KEY_UP) == ('', (
        f'{term.reverse}'
        f'{term.move(0, 0)}spam  '
        f'{term.normal}'
        f'{term.move(1, 0)}eggs  '
        f'{term.move(2, 0)}bacon '
        f'{term.move(3, 0)}ham   '
    ))


def test_action_up_scrolls_to_overflow(KEY_UP, menu_options_long, term):
    """When an up arrow is received, Menu.action() selects the
    previous option. If the selected option is the first visible
    options and the list of option overflows, the list of options
    should scroll up to see the previous option.
    """
    m = menu.Menu(
        options=menu_options_long,
        height=5,
        width=9
    )
    m._overflow_top = True
    m._selected = 3
    m._start = 3
    m._stop = 7
    assert m.action(KEY_UP) == ('', (
        f'{term.move(4, 0)}         '
        f'{term.move(4, 3)}[▼]'
        f'{term.reverse}'
        f'{term.move(1, 0)}bacon '
        f'{term.normal}'
        f'{term.move(2, 0)}ham   '
        f'{term.move(3, 0)}beans '
    ))


def test_action_up_scrolls_near_top_of_overflow(
    KEY_UP, menu_options_long, term
):
    """When a up arrow is received, Menu.action() selects the
    next option. If the selected option is the first visible
    options and the list of option overflows, the list of options
    should scroll up to see the next option. If it scrolls to
    the next to first option, the overflow up marker should be
    replaced with the first option.
    """
    m = menu.Menu(
        options=menu_options_long,
        height=5,
        width=9
    )
    m._overflow_bottom = True
    m._overflow_top = True
    m._selected = 2
    m._start = 2
    m._stop = 5
    assert m.action(KEY_UP) == ('', (
        f'{term.move(0, 0)}         '
        f'{term.move(0, 0)}spam  '
        f'{term.reverse}'
        f'{term.move(1, 0)}eggs  '
        f'{term.normal}'
        f'{term.move(2, 0)}bacon '
        f'{term.move(3, 0)}ham   '
    ))
