"""
text
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
    """
    name: str
    hotkey: Optional[str] = None


# General classes.
class Menu(Scroll, Title):
    """A menu of options."""
    # Magic methods.
    def __init__(
        self,
        options: tuple[Option],
        select_bg: str = '',
        select_fg: str = '',
        content_align_h: str = 'left',
        content_align_v: str = 'top',
        *args, **kwargs
    ) -> None:
        """Initialize an instance of the class.

        :param options: (Optional.) The menu options.
        :param select_bg: (Optional.) A string describing the background
            color of the selection.  See the documentation for `blessed`
            for more detail on the available options.
        :param select_fg: (Optional.) A string describing the foreground
            color of the selection.  See the documentation for `blessed`
            for more detail on the available options.
        :param content_align_h: (Optional.) Horizontal alignment of the
            of the menu options.
        :param content_align_v: (Optional.) Vertical alignment of the
            of the menu options.
        :param footer_align: (Optional.) The horizontal alignment of
            the footer. Valid options include: left, center, right.
        :param footer_frame: (Optional.) Sets whether to add a cap to
            the frame on either side of the footer. You must set the
            `frame_type` parameter if you set this.
        :param footer_text: (Optional.) The footer for the panel.
        :param title_align: (Optional.) The horizontal alignment of
            the title. Valid options include: left, center, and right.
        :param title_bg: (Optional.) The background title of the title.
        :param title_fg: (Optional.) The foreground title of the title.
        :param title_frame: (Optional.) Sets whether to add a cap to
            the frame on either side of the title. You must set the
            `frame_type` parameter if you set this.
        :param title_text: (Optional.) A title for the panel.
        :param content_align_h: (Optional.) The horizontal alignment
            of the contents of the panel. It defaults to center.
        :param content_align_v: (Optional.) The vertical alignment of
            the contents of the penal. It defaults to middle.
        :param content_pad_left: (Optional.) The amount of padding
            between the left inner margin of the panel and the content.
            It is measured as a float between 0.0 and 1.0, where 0.0
            is no padding and 1.0 is the entire width of the panel is
            padding. The default is 0.0.
        :param content_pad_right: (Optional.) The amount of padding
            between the right inner margin of the panel and the content.
            It is measured as a float between 0.0 and 1.0, where 0.0
            is no padding and 1.0 is the entire width of the panel is
            padding. The default is 0.0.
        :param height: The height of the pane.
        :param width: The width of the pane.
        :param term: A blessed.Terminal instance for formatting text
            for terminal display.
        :param origin_y: (Optional.) The terminal row for the top of the
            panel.
        :param origin_x: (Optional.) The terminal column for the left
            side of the panel.
        :param fg: (Optional.) A string describing the foreground color
            of the pane. See the documentation for `blessed` for more
            detail on the available options.
        :param bg: (Optional.) A string describing the background color
            of the pane. See the documentation for `blessed` for more
            detail on the available options.
        :param frame_type: (Optional.) If a string, the string determines
            the frame used for the pane. If None, the pane doesn't have a
            frame.
        :param frame_fg: (Optional.) A string describing the foreground
            color of the frame. See the documentation for `blessed` for
            more detail on the available options. If `fg` is set and
            this is not, the frame will have the `fg` color.
        :param frame_bg: (Optional.) A string describing the background
            color of the frame. See the documentation for `blessed` for
            more detail on the available options. If `bg` is set and
            this is not, the frame will have the `bg` color.
        :return: None.
        :rtype: NoneType
        """
        self.options = options
        self.select_bg = select_bg
        self.select_fg = select_fg
        kwargs['content_align_h'] = content_align_h
        kwargs['content_align_v'] = content_align_v
        super().__init__(*args, **kwargs)

        self._selected = 0
        self._active_keys['KEY_ENTER'] = self._enter
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
        return max(len(opt.name) for opt in self.options)

    @property
    def lines(self) -> list[str]:
        lines = []
        fwidth = self.field_width
        align = '<'
        if self.content_align_h == 'center':
            align = '^'
        if self.content_align_h == 'right':
            align = '>'

        for option in self.options:
            line = f'{option.name:{align}{fwidth}}'
            lines.append(line)

        return lines

    # Public methods.
    def action(self, key: Keystroke) -> tuple[str, str]:
        """React to input from the user.

        :param key: A keystroke from the user.
        :return: A :class:tuple that contains a :class:str containing
            any data that needs to go back to the application and a
            :class:str containing any updates to the terminal.
        :rtype: tuple
        """
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

    def _enter(self, key: Optional[Keystroke] = None) -> str:
        """Return the name of the selected option."""
        return self.options[self._selected].name

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
