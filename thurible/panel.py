"""
panel
~~~~~

Base classes for objects that display data in an area in a terminal.
"""
from typing import Optional

from blessed import Terminal
from blessed.keyboard import Keystroke

from thurible.util import get_terminal, Frame


# Exceptions.
class InvalidTitleAlignmentError(Exception):
    """The value given for the title alignment was invalid."""


class NoFrameTypeForFrameError(Exception):
    """A paramters that requires a frame type was set without setting a
    frame type.
    """


# Base class.
class Panel:
    """A class covering displaying text to the terminal."""
    # Magic methods.
    def __init__(
        self,
        height: Optional[int] = None,
        width: Optional[int] = None,
        term: Optional[Terminal] = None,
        origin_y: int = 0,
        origin_x: int = 0,
        bg: str = '',
        fg: str = '',
        frame_type: Optional[str] = None,
        frame_bg: str = '',
        frame_fg: str = '',
    ) -> None:
        """Initialize an instance of the class.

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
        # Panel protocol.
        self.term = term if term else get_terminal()
        self.height = height if height is not None else self.term.height
        self.width = width if width is not None else self.term.width
        self.origin_y = origin_y
        self.origin_x = origin_x
        self.bg = bg
        self.fg = fg

        # Frame protocol.
        self.frame_type = frame_type
        self.frame_bg = frame_bg
        self.frame_fg = frame_fg

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.height == other.height
            and self.width == other.width
            and self.origin_y == other.origin_y
            and self.origin_x == other.origin_x
            and self.bg == other.bg
            and self.fg == other.fg
            and self.frame_type == other.frame_type
            and self.frame_bg == other.frame_bg
            and self.frame_fg == other.frame_fg
        )

    def __str__(self) -> str:
        """Return a string that will draw the entire display."""
        result = ''
        result += self.clear_contents()
        result += self.frame
        return result

    # Properties
    @property
    def frame(self) -> str:
        """Returns a string that will draw the panel's frame in a
        terminal.
        """
        # Handle frame coloration.
        bg = self.frame_bg if self.frame_bg else self.bg
        fg = self.frame_fg if self.frame_fg else self.fg

        # Create the frame string and return.
        result = ''
        if self.frame_type is not None:
            result += self._frame(
                frame_type=self.frame_type,
                height=self.height,
                width=self.width,
                origin_y=self.origin_y,
                origin_x=self.origin_x,
                foreground=fg,
                background=bg
            )
        return result

    @property
    def inner_height(self) -> int:
        """Returns number of rows available to content within the panel."""
        height = self.height
        if self.frame_type:
            height -= 2
        return height

    @property
    def inner_width(self) -> int:
        """Returns number of columns available to content within the
        panel.
        """
        width = self.width
        if self.frame_type:
            width -= 2
        return width

    @property
    def inner_y(self) -> int:
        """Returns the position in the terminal of the first row
        available to content within the panel.
        """
        y = self.origin_y
        if self.frame_type:
            y += 1
        return y

    @property
    def inner_x(self) -> int:
        """Returns the position in the terminal of the first column
        available to content within the panel.
        """
        x = self.origin_x
        if self.frame_type:
            x += 1
        return x

    # Public methods.
    def action(self, key: Keystroke) -> tuple[str, str]:
        """React to input from the user.

        :param key: A keystroke from the user.
        :return: A :class:tuple that contains a :class:str containing
            any data that needs to go back to the application and a
            :class:str containing any updates to the terminal.
        :rtype: tuple
        """
        data = str(key)
        update = ''
        return (data, update)

    def clear_contents(self) -> str:
        """Return a string that will clear the contents of the panel.

        :return: A :class:str that fills the interior of the panel
            with spaces.
        :rtype: str
        """
        # Set up.
        height = self.inner_height
        width = self.inner_width
        y = self.inner_y
        x = self.inner_x
        color = self._get_color(self.fg, self.bg)
        result = color

        # Create the clearing string and return.
        for i in range(height):
            result += self.term.move(y + i, x) + ' ' * width
        if color:
            result += self.term.normal
        return result

    # Private helper methods.
    def _get_color(self, fg: str = '', bg: str = '') -> str:
        color = fg
        if color and bg:
            color += f'_on_{bg}'
        elif bg:
            color += f'on_{bg}'
        return getattr(self.term, color)

    def _frame(
        self,
        frame_type: str,
        height: int,
        width: int,
        origin_y: int = 0,
        origin_x: int = 0,
        foreground: str = '',
        background: str = ''
    ) -> str:
        frame = Frame(frame_type)
        result = self._get_color(foreground, background)
        result += (
            self.term.move(origin_y, origin_x)
            + frame.ltop
            + frame.top * (width - 2)
            + frame.rtop
        )
        for y in range(origin_y + 1, origin_y + height - 1):
            line = (
                self.term.move(y, origin_x) + frame.side
                + self.term.move(y, origin_x + width - 1) + frame.side
            )
            result += line
        result += (
            self.term.move(origin_y + height - 1, origin_x)
            + frame.lbot
            + frame.bot * (width - 2)
            + frame.rbot
        )
        if background or foreground:
            result += self.term.normal
        return result


# Protocols.
class Content(Panel):
    """A panel that contains text content."""
    # Magic methods.
    def __init__(
        self,
        content_align_h: str = 'center',
        content_align_v: str = 'middle',
        content_pad_left: float = 0.0,
        content_pad_right: float = 0.0,
        *args, **kwargs
    ) -> None:
        """Initialize an instance of the class.

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
        self.content_align_h = content_align_h
        self.content_align_v = content_align_v
        self.content_pad_left = content_pad_left
        self.content_pad_right = content_pad_right
        super().__init__(*args, **kwargs)

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            super().__eq__(other)
            and self.content_align_h == other.content_align_h
            and self.content_align_v == other.content_align_v
            and self.content_pad_left == other.content_pad_left
            and self.content_pad_right == other.content_pad_right
        )

    # Properties.
    @property
    def content_width(self) -> int:
        width = self.inner_width
        width -= self._offset_left
        width -= self._offset_right
        return width

    @property
    def content_x(self) -> int:
        x = self.inner_x
        x += self._offset_left
        return x

    @property
    def lines(self) -> list[str]:
        """Returns the content of the panel as a list of strings, where
        each string represents a row in the panel.
        """
        # This is an abstract version of the property. It will need to
        # be reimplemented for the classes that follow the Content
        # protocol.
        return ['',]

    @property
    def _offset_left(self) -> int:
        offset = super().inner_width * self.content_pad_left
        return int(offset)

    @property
    def _offset_right(self) -> int:
        offset = super().inner_width * self.content_pad_right
        return int(offset)

    # Private helper methods.
    def _align_h(self, align: str, length: int, width: int) -> int:
        """Return the amount offset the column for the horizontal
        alignment.
        """
        if align == 'left':
            x_mod = 0
        elif align == 'center':
            h_space = width - length
            x_mod = h_space // 2
        elif align == 'right':
            h_space = width - length
            x_mod = h_space
        return x_mod

    def _align_v(self, align: str, length: int, height: int) -> int:
        """Return the amount offset the column for the vertical
        alignment.
        """
        if align == 'middle':
            v_space = height - length
            y_mod = v_space // 2
        elif align == 'top':
            y_mod = 0
        elif align == 'bottom':
            v_space = height - length
            y_mod = v_space
        return y_mod


class Scroll(Content):
    """A panel where the content can be scrolled."""
    def __init__(
        self,
        *args, **kwargs
    ) -> None:
        """Initialize an instance of the class.

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
        super().__init__(*args, **kwargs)

        self._lines: list[str] = []
        self._ofbot = '[▼]'
        self._oftop = '[▲]'
        self._overflow_bottom = False
        self._overflow_top = False
        self._start = 0
        self._stop = self.inner_height
        self._wrapped_width = -1

        self._active_keys = {
            'KEY_END': self._end,
            'KEY_DOWN': self._line_down,
            'KEY_HOME': self._home,
            'KEY_PGDOWN': self._page_down,
            'KEY_PGUP': self._page_up,
            'KEY_UP': self._line_up,
        }

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return super().__eq__(other)

    # Property.
    @property
    def inner_height(self) -> int:
        height = super().inner_height
        if self._overflow_bottom:
            height -= 1
        if self._overflow_top:
            height -= 1
        return height

    @property
    def inner_y(self) -> int:
        y = super().inner_y
        if self._overflow_top:
            y += 1
        return y

    # Public methods.
    def action(self, key: Keystroke) -> tuple[str, str]:
        # These are the results that are returned.
        data = ''
        update = ''

        # Initial set up.
        height = self.inner_height
        width = self.inner_width
        y = self.inner_y
        x = self.inner_x
        lines = self.lines
        length = len(lines)

        # Handle input.
        if length <= height and key.name in self._active_keys:
            ...
        elif key.name in self._active_keys:
            action = self._active_keys[key.name]
            action()
            update, height, y = self._flow(
                update,
                length,
                height,
                width,
                y, x
            )
            self._overscroll(length, height)
            update += self.clear_contents()
            update += self._visible(lines, width, y, x)
        else:
            data = str(key)

        # Return the results.
        return data, update

    # Private action handlers.
    def _end(self, key: Optional[Keystroke] = None) -> str:
        """Scroll to the bottom of the content."""
        length = len(self.lines)
        self._start = length - self.inner_height
        self._stop = length
        return ''

    def _home(self, key: Optional[Keystroke] = None) -> str:
        """Scroll to the top of the content."""
        self._start = 0
        self._stop = self.inner_height
        return ''

    def _line_down(self, key: Optional[Keystroke] = None) -> str:
        """Scroll a line down in the content."""
        self._start += 1
        self._stop += 1
        return ''

    def _line_up(self, key: Optional[Keystroke] = None) -> str:
        """Scroll a line up in the content."""
        self._start -= 1
        self._stop -= 1
        return ''

    def _page_down(self, key: Optional[Keystroke] = None) -> str:
        """Scroll down one page in the content."""
        height = self.inner_height
        self._start += height
        self._stop += height
        if not self._overflow_top:
            self._start -= 1
            self._stop -= 1
        return ''

    def _page_up(self, key: Optional[Keystroke] = None) -> str:
        """Scroll up one page in the content."""
        height = self.inner_height
        self._start -= height
        self._stop -= height
        if not self._overflow_bottom:
            self._start += 1
            self._stop += 1
        return ''

    # Private helper methods.
    def _flow(
        self,
        update: str,
        length: int,
        height: int,
        width: int,
        y: int,
        x: int
    ) -> tuple[str, int, int]:
        """Manage text that overflows the visible answer."""
        if self._stop >= length - 1 and self._overflow_bottom:
            self._stop += 1
            self._overflow_bottom = False
            height += 1
            end = y + height - 1
            update += self._get_color(self.fg, self.bg)
            update += self.term.move(end, x) + ' ' * width
            if self.fg or self.bg:
                update += self.term.normal
        if self._stop < length and not self._overflow_bottom:
            self._stop -= 1
            self._overflow_bottom = True
            height -= 1
            end = y + height
            x_mod = self._align_h('center', len(self._ofbot), width)
            update += self._get_color(self.fg, self.bg)
            update += self.term.move(end, x) + ' ' * width
            update += self.term.move(end, x + x_mod) + self._ofbot
            if self.fg or self.bg:
                update += self.term.normal
        if self._start <= 1 and self._overflow_top:
            self._start -= 1
            self._overflow_top = False
            height += 1
            y -= 1
            update += self._get_color(self.fg, self.bg)
            update += self.term.move(y, x) + ' ' * width
            if self.fg or self.bg:
                update += self.term.normal
        if self._start > 0 and not self._overflow_top:
            self._start += 1
            self._overflow_top = True
            x_mod = self._align_h('center', len(self._oftop), width)
            update += self._get_color(self.fg, self.bg)
            update += self.term.move(y, x) + ' ' * width
            update += self.term.move(y, x + x_mod) + self._oftop
            if self.fg or self.bg:
                update += self.term.normal
            height -= 1
            y += 1
        return update, height, y

    def _overscroll(self, length: int, height: int) -> None:
        """Manage situations where the visible area is scrolled beyond
        the text.
        """
        if self._start < 0:
            self._start = 0
            self._stop = height
        elif self._stop > length and length > height:
            self._stop = length
            self._start = self._stop - height
        elif self._stop > length:
            self._stop = length
            self._start = 0

    def _visible(self, lines: list[str], width: int, y: int, x: int) -> str:
        """Output the lines in the display."""
        update = ''
        update += self._get_color(self.fg, self.bg)
        for i, line in enumerate(lines[self._start: self._stop]):
            x_mod = self._align_h(self.content_align_h, len(line), width)
            update += self.term.move(y + i, x + x_mod) + line
        if self.fg or self.bg:
            update += self.term.normal
        return update


class Title(Panel):
    """A panel with a title."""
    # Magic methods.
    def __init__(
        self,
        footer_align: str = 'left',
        footer_frame: bool = False,
        footer_text: str = '',
        title_align: str = 'left',
        title_bg: str = '',
        title_fg: str = '',
        title_frame: bool = False,
        title_text: str = '',
        *args, **kwargs
    ) -> None:
        """Initialize an instance of the class.

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
        super().__init__(*args, **kwargs)
        self.footer_text = footer_text
        self.footer_align = footer_align
        self.footer_frame = footer_frame
        self.title_text = title_text
        self.title_align = title_align
        self.title_frame = title_frame
        self.title_bg = title_bg
        self.title_fg = title_fg

        self._ofr = '[▸]'

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            super().__eq__(other)
            and self.footer_text == other.footer_text
            and self.footer_align == other.footer_align
            and self.footer_frame == other.footer_frame
            and self.title_text == other.title_text
            and self.title_align == other.title_align
            and self.title_frame == other.title_frame
            and self.title_bg == other.title_bg
            and self.title_fg == other.title_fg
        )

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return f"{name}(title_text='{self.title_text}')"

    def __str__(self) -> str:
        """Return a string that will draw the entire display."""
        result = super().__str__()
        result += self.title
        result += self.footer
        return result

    # Properties.
    @property
    def footer(self) -> str:
        """Returns a string to write the footer of the panel to the
        terminal.
        """
        y = self.origin_y + self.height - 1
        text = self.footer_text
        frame = self.footer_frame
        return self._title(text, self.footer_align, y, frame)

    @property
    def footer_frame(self) -> bool:
        return self._Title__footer_frame

    @footer_frame.setter
    def footer_frame(self, value: bool) -> None:
        if value and not self.frame_type:
            msg = 'You must set frame_type if you set footer_frame.'
            raise NoFrameTypeForFrameError(msg)
        self._Title__footer_frame = value

    @property
    def frame(self) -> str:
        result = super().frame
        if not result:
            height = self.height
            width = self.width
            y = self.origin_y
            x = self.origin_x
            bg = self.title_bg if self.title_bg else self.bg
            fg = self.title_fg if self.title_fg else self.fg
        if not result and self.title_text:
            result += self._get_color(fg, bg)
            result += self.term.move(y, x) + ' ' * width
            if bg or fg:
                result += self.term.normal
        if not result and self.footer_text:
            result += self._get_color(fg, bg)
            result += self.term.move(y + height - 1, x) + ' ' * width
            if bg or fg:
                result += self.term.normal
        return result

    @property
    def inner_height(self) -> int:
        height = super().inner_height
        if self.frame_type is None and self.title_text:
            height -= 1
        if self.frame_type is None and self.footer_text:
            height -= 1
        return height

    @property
    def inner_y(self) -> int:
        y = super().inner_y
        if self.frame_type is None and self.title:
            y += 1
        return y

    @property
    def title(self) -> str:
        """Returns a string to write the title of the panel to the
        terminal.
        """
        text = self.title_text
        frame = self.title_frame
        return self._title(text, self.title_align, self.origin_y, frame)

    @property
    def title_frame(self) -> bool:
        return self._Title__title_frame

    @title_frame.setter
    def title_frame(self, value: bool) -> None:
        if value and not self.frame_type:
            msg = 'You must set frame_type if you set title_frame.'
            raise NoFrameTypeForFrameError(msg)
        self._Title__title_frame = value

    # Private helper methods.
    def _title(
        self,
        title: str,
        align: str,
        y: int,
        frame: bool = False
    ) -> str:
        """Build and return a string to write the title of the panel
        to the terminal.
        """
        result = ''

        # Bail out early if there is no title.
        if not title:
            return result

        # Set up.
        x = self.inner_x
        width = self.inner_width

        # Set the color and frame for the title.
        if len(title) >= width:
            title = title[:width - 3] + self._ofr
        title = self._title_color(title)
        if isinstance(self.frame_type, str) and frame:
            title = self._title_frame(title, self.frame_type)

        # Align the title.
        if align == 'left':
            ...
        elif align == 'center':
            space = width - len(title)
            x += space // 2
        elif align == 'right':
            x += width - len(title)
        else:
            msg = f'Invalid title alignment: {self.title_align}.'
            raise InvalidTitleAlignmentError(msg)

        # Create the title and return.
        result += self.term.move(y, x) + title
        return result

    def _title_color(self, title: str) -> str:
        """Apply the title color to a title or footer."""
        bg = self.title_bg if self.title_bg else self.bg
        fg = self.title_fg if self.title_fg else self.fg
        result = self._get_color(fg, bg)
        result += title
        if bg or fg:
            result += self.term.normal
        return result

    def _title_frame(self, title: str, frame_type: str) -> str:
        """Apply the frame cap to the title or footer."""
        frame = Frame(frame_type)
        bg = self.frame_bg if self.frame_bg else self.bg
        fg = self.frame_fg if self.frame_fg else self.fg
        color = self._get_color(fg, bg)
        normal = self.term.normal if color else ''
        lside = color + frame.rside + normal
        rside = color + frame.lside + normal
        return lside + title + rside
