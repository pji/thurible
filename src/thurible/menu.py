"""
menu
~~~~

An object for displaying a text area in a terminal.
"""
from dataclasses import dataclass
from typing import Optional

from blessed import Terminal
from blessed.keyboard import Keystroke

from thurible.panel import Scroll, Title
from thurible.util import Box


# Utility classes.
@dataclass
class Option:
    """A command or menu option.

    :param name: The name of the option.
    :param hotkey: (Optional.) A hotkey that can be used to invoke
        the option.
    :returns: A :class:`thurible.Option` object.
    :rtype: thurible.Option
    :usage:
        To create a menu option "spam" with the hotkey of "s":

        .. testcode::

            import thurible

            option = thurible.Option('spam', hotkey='s')
    """
    name: str
    hotkey: Optional[str] = None


# General classes.
class Menu(Scroll, Title):
    """Create a new :class:`thurible.Menu` object. This class provides
    a list of options the user can select. As a subclass of
    :class:`thurible.panel.Scroll` and :class:`thurible.panel.Title`,
    it can also take those parameters and has those public methods,
    properties, and active keys.

    :param options: A sequence of :class:`thurible.Option` objects
        defining the options available to the user.
    :param option_align_h: (Optional.) The horizontal alignment
        of the options within the area that would be highlighted when
        the option is highlighted. If you think of each option as a
        button, it's how the text is aligned on the face of the button.
        It defaults to "left".
    :param select_bg: (Optional.) The background color used to
        highlight an option.
    :param select_fg: (Optional.) The foreground color used to
        highlight an option.
    :param content_align_h: (Optional.) The horizontal alignment
        of the contents of the panel. It defaults to "left". See
        :class:`thurible.panel.Content` for more information.
    :param content_align_v: (Optional.) The vertical alignment
        of the contents of the panel. It defaults to "top".
    :return: A :class:`thurible.Menu` object.
    :rtype: thurible.Menu
    :usage:
        To create a minimal new :class:`thurible.Menu` object with
        two options:

        .. testcode::

            import thurible

            opt1 = thurible.Option('spam', hotkey='s')
            opt2 = thurible.Option('eggs', hotkey='e')
            menu = thurible.Menu([opt1, opt2])

        Information on the sizing of :class:`thurible.Menu`
        objects can be found in the :ref:`sizing` section below.

    :active keys:
        :class:`thurible.Menu` adds the additional active key:

            *   KEY_ENTER: Select the highlighted option.
            *   Optional hot keys to highlight the options, as defined in
                the :class:`thurible.Option` object for the option.

        :class:`thurible.Menu` modifies the behavior of the following
        active keys:

            *   KEY_END: Highlight the last option, scrolling if needed.
            *   KEY_DOWN: Highlight the next option, scrolling if needed.
            *   KEY_HOME: Highlight the first option, scrolling if needed.
            *   KEY_PGDOWN: Scroll to and highlight the option one screen
                down.
            *   KEY_PGUP: Scroll to and highlight the option one screen up.
            *   KEY_UP: Highlight the previous option, scrolling if needed.

        For more information on active keys, see :ref:`active`.

    """
    # Magic methods.
    def __init__(
        self,
        options: tuple[Option],
        option_align_h: str = 'left',
        select_bg: str = '',
        select_fg: str = '',
        content_align_v: str = 'top',
        *args, **kwargs
    ) -> None:
        self.options = options
        self.option_align_h = option_align_h
        self.select_bg = select_bg
        self.select_fg = select_fg
        if (
            'content_pad_left' not in kwargs
            and 'conent_pad_right' not in kwargs
            and 'content_align_h' not in kwargs
        ):
            kwargs['content_align_h'] = 'left'
        kwargs['content_align_v'] = content_align_v
        super().__init__(*args, **kwargs)

        self._selected = 0
        self._active_keys['KEY_ENTER'] = self._select
        for option in self.options:
            hotkey = f"'{option.hotkey}'"
            self._active_keys[hotkey] = self._hotkey

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            super().__eq__(other)
            and self.options == other.options
            and self.select_bg == other.select_bg
            and self.select_fg == other.select_fg
        )

    def __str__(self) -> str:
        """Return a string that will draw the entire panel."""
        # Set up.
        lines = self.lines
        length = len(lines)
        height = self.inner_height
        width = self.content_width
        y = self.inner_y
        x = self.content_x
        self._start = 0
        self._stop = height
        result = super().__str__()

        # Create the display string and return.
        y += self._align_v(self.content_align_v, length, height)
        result, height, y = self._flow(result, length, height, width, y, x)
        self._overscroll(length, height)
        result += self._visible(lines, width, y, x)
        return result

    # Properties.
    @property
    def field_width(self) -> int:
        """The width of the highlightable area of each option as
        determined by the option with the most characters.

        :return: A :class:`int` object.
        :rtype: int
        """
        return max(len(opt.name) for opt in self.options)

    @property
    def lines(self) -> list[str]:
        """A :class:`list` of :class:`str` objects used to display
        the panel in the terminal.

        :return: A :class:`list` object of :class:`str` objects.
        :rtype: list
        """
        lines = []
        fwidth = self.field_width
        align = '<'
        if self.option_align_h == 'center':
            align = '^'
        if self.option_align_h == 'right':
            align = '>'

        for option in self.options:
            line = f'{option.name:{align}{fwidth}}'
            lines.append(line)

        return lines

    # Public methods.
    def action(self, key: Keystroke) -> tuple[str, str]:
        # These are the results that are returned.
        data = ''
        update = ''

        # Initial set up.
        height = self.inner_height
        width = self.content_width
        y = self.inner_y
        x = self.content_x
        lines = self.lines
        length = len(lines)

        # Handle input.
        if repr(key) in self._active_keys:
            handler = self._active_keys[repr(key)]
            data = handler(key)
        else:
            data = str(key)

        # Create any needed updates to the terminal.
        if not data:
            update, height, y = self._flow(
                update,
                length,
                height,
                width,
                y, x
            )
            self._overscroll(length, height)
            update += self._visible(lines, width, y, x)

        # Return the results.
        return data, update

    # Private action handlers.
    def _end(self, key: Optional[Keystroke] = None) -> str:
        """Select the last option and scroll to it."""
        length = len(self.lines)
        self._selected = length - 1
        self._start = length - self.inner_height
        self._stop = length
        return ''

    def _home(self, key: Optional[Keystroke] = None) -> str:
        """Select the first option and scroll to it."""
        self._selected = 0
        self._start = 0
        self._stop = self.inner_height
        return ''

    def _hotkey(self, key: Optional[Keystroke] = None) -> str:
        hotkeys = [option.hotkey for option in self.options]
        length = len(self.options)
        height = self.inner_height
        self._selected = hotkeys.index(str(key))
        if self._start > self._selected:
            self._start = self._selected
            self._stop = self._start + height
        elif self._stop <= self._selected:
            self._stop = self._selected
            self._start = self._stop - height
            if length > height and self._selected == length - 2:
                self._start += 1
                self._stop += 1
        return ''

    def _line_down(self, key: Optional[Keystroke] = None) -> str:
        """Select the next option."""
        if self._selected < len(self.options) - 1:
            self._selected += 1
        if self._selected >= self._stop:
            self._start += 1
            self._stop += 1
        return ''

    def _line_up(self, key: Optional[Keystroke] = None) -> str:
        """Select the pervious option."""
        if self._selected > 0:
            self._selected -= 1
        if self._selected < self._start:
            self._start -= 1
            self._stop -= 1
        return ''

    def _page_down(self, key: Optional[Keystroke] = None) -> str:
        """Scroll down one page in the content."""
        height = self.inner_height
        self._selected += height
        self._start += height
        self._stop += height
        if not self._overflow_top:
            self._start -= 1
            self._stop -= 1
        return ''

    def _page_up(self, key: Optional[Keystroke] = None) -> str:
        """Scroll up one page in the content."""
        height = self.inner_height
        self._selected -= height
        self._start -= height
        self._stop -= height
        if not self._overflow_bottom:
            self._start += 1
            self._stop += 1
        return ''

    def _select(self, key: Optional[Keystroke] = None) -> str:
        """Return the name of the selected option."""
        return self.options[self._selected].name

    # Private helper methods.
    def _color_selection(self) -> str:
        result: str = self.term.reverse
        if self.select_bg or self.select_fg:
            result = self._get_color(self.select_fg, self.select_bg)
        return result

    def _overscroll(self, length: int, height: int) -> None:
        if self._selected < 0:
            self._selected = 0
        elif self._selected >= length:
            self._selected = length - 1
        super()._overscroll(length, height)

    def _visible(self, lines: list[str], width: int, y: int, x: int) -> str:
        """Output the lines in the display."""
        # Set the base colors for the menu options.
        update = self._get_color(self.fg, self.bg)

        # Create the visible options.
        for i, line in enumerate(lines[self._start: self._stop]):
            x_mod = self._align_h(self.content_align_h, len(line), width)

            # Use the selection colors if the option is selected. The
            # `opt_index` variable here translates working row in the
            # terminal display to the index of the items in the list
            # of menu options. It's needed because we aren't tracking
            # the selection in the options list itself.
            opt_index = i + self._start
            if opt_index == self._selected:
                update += self._color_selection()

            # Create the option.
            update += self.term.move(y + i, x + x_mod) + line

            # Revert to the base colors if this option was selected.
            if opt_index == self._selected and not (self.fg or self.bg):
                update += self.term.normal
            elif opt_index == self._selected:
                update += self.term.normal
                update += self._get_color(self.fg, self.bg)

        # End the coloring so we don't have to worry about it the next
        # time we print a string, and return the options.
        if self.fg or self.bg:
            update += self.term.normal
        return update
