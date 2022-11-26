"""
panel
~~~~~

Base classes for objects that display data in an area in a terminal.
"""
from typing import Optional

from blessed import Terminal
from blessed.keyboard import Keystroke

from thurible.util import Box, get_terminal


# Exceptions.
class InvalidDimensionsError(Exception):
    """The parameters that determine the relative width or height
    must add up to one.
    """


class InvalidTitleAlignmentError(Exception):
    """The value given for the title alignment was invalid."""


class NoFrameTypeForFrameError(Exception):
    """A paramters that requires a frame type was set without setting a
    frame type.
    """


class PanelPaddingAndAlignmentSetError(Exception):
    """You cannot set both panel padding and alignment."""


# Base class.
class Panel:
    """A class covering displaying text to the terminal."""
    # Magic methods.
    def __init__(
        self,
        height: Optional[int] = None,
        width: Optional[int] = None,
        term: Optional[Terminal] = None,
        origin_y: Optional[int] = None,
        origin_x: Optional[int] = None,
        bg: str = '',
        fg: str = '',
        panel_pad_bottom: Optional[float] = None,
        panel_pad_left: Optional[float] = None,
        panel_pad_right: Optional[float] = None,
        panel_pad_top: Optional[float] = None,
        panel_relative_height: Optional[float] = None,
        panel_relative_width: Optional[float] = None,
        panel_align_h: Optional[str] = None,
        panel_align_v: Optional[str] = None
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
        :param panel_pad_top: (Optional.) Distance between the
            `origin_y` of the panel and the top of the interior of the
            panel. It is a percentage expressed as a :class:float
            between 0.0 and 1.0, inclusive. See Sizing below for more
            information.
        :param panel_relative_height: (Optional.) The height of the
            interior of the panel in comparison of the full `height` of
            the panel. It is a percentage expressed as a :class:float
            between 0.0 and 1.0, inclusive. See Sizing below for more
            information.
        :param panel_pad_bottom: (Optional.) Distance between the
            full `height` of the panel and the interior of the panel.
            It is a percentage expressed as a :class:float between 0.0
            and 1.0, inclusive. See Sizing below for more information.
        :param panel_pad_left: (Optional.) Distance between the
            `origin_x` of the panel and the left side of the interior
            of the panel. It is a percentage expressed as a :class:float
            between 0.0 and 1.0, inclusive. See Sizing below for more
            information.
        :param panel_relative_width: (Optional.) The width of the
            interior of the panel in comparison of the full `width` of
            the panel. It is a percentage expressed as a :class:float
            between 0.0 and 1.0, inclusive. See Sizing below for more
            information.
        :param panel_pad_right: (Optional.) Distance between the full
            `width` of the panel and the right side of the interior of
            the panel. It is a percentage expressed as a :class:float
            between 0.0 and 1.0, inclusive. See Sizing below for more
            information.
        :param panel_align_h: (Optional.) If the interior of the panel
            is smaller than the full `width` of the panel, this sets
            how the interior of the panel is aligned within the full
            height. It is a percentage expressed as a :class:float
            between 0.0 and 1.0, inclusive. See Sizing below for more
            information.
        :param panel_align_v: (Optional.) If the interior of the panel
            is smaller than the full `width` of the panel, this sets
            how the interior of the panel is aligned within the full
            height. It is a percentage expressed as a :class:float
            between 0.0 and 1.0, inclusive. See Sizing below for more
            information.
        :return: None.
        :rtype: NoneType

        Sizing
        ======
        Panels attempt to allow for the relative sizing of an element
        within a terminal. What does that mean?

        A terminal window has a size in rows and columns. These rows
        and columns are measured in relation to a fixed-width character.
        A row is the height of one character. A column is the width of
        one character. For reasons that go back to the era of punch
        cards and hardware terminals, the common default size of a
        terminal window is 24 rows by 80 columns.

        However, terminal widows do not have to be that standard size.
        Most terminal emulators that I've used allow you to set any
        size you want for the size of the terminal window, and you can
        resize the window after you open it. That creates a problem if
        you are trying to create a consistent interface for a terminal
        application. Sure, you can usually assume that a terminal is
        going to be 24×80, but if you run into a terminal that is
        48×132, things might get weird.

        Panel tries to solve that by allowing you to set the size of
        a panel relative to the terminal window, no matter what size
        that terminal window is. Now, there are some limitation to that.
        If the terminal window is 1×1, there isn't much that can be
        shown in that terminal. However, it still should be useful for
        most terminal sizes you are going to run into.

        The Absolute Sizing Model
        -------------------------
        To position the panel in the terminal, `thurible` managers start
        with the absolute position. The absolute position is determined
        by the following attributes:

        height
            The number of rows from the top of the panel to the bottom.
            If you don't specify a height, it will default to the
            total number of rows in the current terminal window.
        width
            The number of columns from the left side of the panel to
            the right side. If you don't specify a width, it will
            default to the number of columns in the current terminal
            window.
        origin_x
            The left-most column of the panel. If you don't specify an
            origin_x, it will default to the left-most row of the
            terminal window.
        origin_y
            The top-most row of the panel. If you don't specify an
            origin_y, it will default to the top-most row of the
            terminal window.

        For the most part, it's best not to set these manually, and just
        let it default to fill the entire terminal window. However, if
        you have some case where you need to manually set them, such as
        simplifying unit tests, you can do so.

        The Relative Sizing Model
        -------------------------
        After determining the absolute position of the panel, `thurible`
        then uses the following attributes to determine where the
        interior space of the panel is located relative to the absolute
        position of the panel in the terminal window.

        The horizontal positioning attributes are:

        *	panel_pad_left
        *   panel_relative_width
        *   panel_pad_right

        The vertical positioning attributes are:

        *   panel_pad_top
        *   panel_relative_height
        *   panel_pad_bottom

        Each of those takes a value from 0.0 to 1.0, inclusive, that
        sets what percentage of the absolute size of the panel is
        taken up by that part of the relative size. For example, let's
        say you create the following panel::

            >>> panel = Panel(
            >>>     origin_x=0,
            >>>     width=80,
            >>>     panel_pad_left=0.2
            >>> )

        The absolute left side of the panel is the left-most column of
        the terminal window (in Python that's referred to as column 0,
        those curses programming will often call it column 1). The
        absolute width of the terminal is 80 columns. However, the
        interior of the frame starts 20% of the total width of the panel
        from the absolute left-most column, which is column::

            80 * 0.2 = 16

        The interior then takes of the remaining 80% of the absolute
        width of the panel, or::

            80 * 0.8 = 64

        As shown in the example, you do not need to set all three of
        the relative positioning attribute for each dimension. In most
        cases, it's only necessary to set one per dimension.

        .. note:
            If you do set all three of the relative positioning
            attributes for a dimension, you must ensure that the sum
            of all three attributes equals 1.0. Because floating-point
            math is involved, it's theoretically possible that some
            values that look like they should add to 1.0 won't add to
            1.0. The best way to avoid that is never set all three
            of the attributes for a dimension. Set one, or at most
            two, and let the panel object calculate the rest for you.

        While you can set any of the three relative positional
        attributes, it is recommended that you use ones that set the
        relative interior sizes:

        *   panel_relative_height
        *   panel_relative_width

        Then, instead of setting any of the "panel_pad" attributes, set
        the alignment attribute for the dimension:

        *   panel_align_h
        *   panel_align_v

        Setting those attributes will align the relative interior area
        of the panel with the absolute area of the panel.

        The valid values when setting panel_align_h are:

        *   left
        *   center
        *   right

        The valid values when setting panel_align_v are:

        *   top
        *   middle
        *   bottom

        For example, if you create the following panel::

            >>> panel = Panel(
            >>>     panel_relative_height=0.25,
            >>>     panel_relative_width=0.25,
            >>>     panel_align_h='right',
            >>>     panel_align_v='bottom'
            >>> )

        You will get a panel that will fill the bottom-right quarter of
        the terminal window.

        .. note:
            You cannot set panel alignment attributes (panel_align_h
            and panel_align_v) and the panel padding attributes (any of
            the panel_pad_* attributes) at the same time. The alignment
            attributes use the panel padding attributes to position the
            interior of the panel, so setting both of them would create
            a conflict that could lead to unexpected behavior.
        """
        # Panel protocol.
        self.term = term if term else get_terminal()
        self._set_relative_horizontal_dimensions(
            panel_pad_left,
            panel_relative_width,
            panel_pad_right,
            panel_align_h
        )
        self._set_relative_vertical_dimensions(
            panel_pad_top,
            panel_relative_height,
            panel_pad_bottom,
            panel_align_v
        )
        self.height = height if height is not None else self.term.height
        self.width = width if width is not None else self.term.width
        self.origin_y = origin_y if origin_y else 0
        self.origin_x = origin_x if origin_x else 0
        self.bg = bg
        self.fg = fg

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
        )

    def __str__(self) -> str:
        """Return a string that will draw the entire display."""
        result = ''
        result += self.clear_contents()
        return result

    # Properties
    @property
    def inner_height(self) -> int:
        """Returns number of rows available to content within the panel."""
        height = self.height
        height -= self._panel_pad_offset_top
        height -= self._panel_pad_offset_bottom
        return height

    @property
    def inner_width(self) -> int:
        """Returns number of columns available to content within the
        panel.
        """
        width = self.width
        width -= self._panel_pad_offset_left
        width -= self._panel_pad_offset_right
        return width

    @property
    def inner_x(self) -> int:
        """Returns the position in the terminal of the first column
        available to content within the panel.
        """
        return self.origin_x + self._panel_pad_offset_left

    @property
    def inner_y(self) -> int:
        """Returns the position in the terminal of the first row
        available to content within the panel.
        """
        return self.origin_y + self._panel_pad_offset_top

    @property
    def _panel_pad_offset_bottom(self) -> int:
        offset = self.height * self.panel_pad_bottom
        return int(offset)

    @property
    def _panel_pad_offset_left(self) -> int:
        offset = self.width * self.panel_pad_left
        return int(offset)

    @property
    def _panel_pad_offset_right(self) -> int:
        offset = self.width * self.panel_pad_right
        return int(offset)

    @property
    def _panel_pad_offset_top(self) -> int:
        offset = self.height * self.panel_pad_top
        return int(offset)

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

    def _set_relative_dimenstion(
        self,
        left: Optional[float] = None,
        width: Optional[float] = None,
        right: Optional[float] = None,
        align: Optional[str] = None,
        align_default: str = 'center',
        alignments: tuple[str, str, str] = ('left', 'center', 'right'),
        attr_names: tuple[str, str, str] = (
            'panel_pad_left',
            'panel_relative_width',
            'panel_pad_right',
        )
    ) -> tuple[float, float, float, str]:
        # This function needs to check which parameters are None a lot.
        # So, the answer to that is stored in this tuple to help
        # reduce the verbosity of the rest of the function.
        were_set = (left is not None, width is not None, right is not None)
        LEFT, WIDTH, RIGHT = 0, 1, 2

        # Since we aren't directly checking these values to see if they
        # are None, mypy will get confused. So, replace Nones with 0.0
        # to keep mypy happy.
        left = 0.0 if left is None else left
        width = 0.0 if width is None else width
        right = 0.0 if right is None else right

        # If both padding and alignment are set, raise an exception
        # because the intended behavior of the panel would be ambiguous.
        if align is not None and any((were_set[LEFT], were_set[RIGHT])):
            msg = 'Cannot set both panel padding and panel alignment.'
            raise PanelPaddingAndAlignmentSetError(msg)

        # If only width was set and align wasn't, set align to the default.
        elif align is None:
            align = align_default

        # If none are set, use the default values.
        if not any(were_set):
            left = 0.0
            right = 0.0
            width = 1.0

        # If all three values are set, they must add up to one.
        elif all(were_set) and left + right + width != 1.0:
            msg = (
                f'If {attr_names[LEFT]}, {attr_names[RIGHT]}, and '
                f'{attr_names[WIDTH]} are set, the sum of '
                'the three must equal one. The given values were: '
                f'{attr_names[LEFT]}={left}, '
                f'{attr_names[RIGHT]}={right}, '
                f'and {attr_names[WIDTH]}={width}.'
            )
            raise InvalidDimensionsError(msg)

        # If only left was set, the rest goes to width.
        elif sum(were_set) == 1 and were_set[LEFT]:
            width = 1.0 - left
            right = 0.0

        # If only width was set, the padding depends on the alignment.
        elif sum(were_set) == 1 and were_set[WIDTH]:
            total = 1.0 - width
            if align == alignments[LEFT]:
                left = 0.0
                right = total
            elif align == alignments[RIGHT]:
                left = total
                right = 0.0
            else:
                left = total / 2
                right = total / 2

        # If only right was set, the rest goes to width.
        elif sum(were_set) == 1 and were_set[RIGHT]:
            left = 0.0
            width = 1.0 - right

        # If only left wasn't set, width is everything that remains.
        elif sum(were_set) == 2 and not were_set[LEFT]:
            left = 1.0 - width - right

        # If only width wasn't set, width is everything that's not pad.
        elif sum(were_set) == 2 and not were_set[WIDTH]:
            width = 1.0 - left - right

        # If only right wasn't set, right is everything that remains.
        elif sum(were_set) == 2 and not were_set[RIGHT]:
            right = 1.0 - left - width

        # Return the values.
        return left, width, right, align

    def _set_relative_horizontal_dimensions(
        self,
        left: Optional[float] = None,
        width: Optional[float] = None,
        right: Optional[float] = None,
        align: Optional[str] = None,
    ) -> None:
        """Ensure the horizontal relative dimensions are set correctly."""
        # Calculate the correct values.
        left, width, right, align = self._set_relative_dimenstion(
            left,
            width,
            right,
            align
        )

        # Set the attributes.
        self.panel_pad_left = left
        self.panel_relative_width = width
        self.panel_pad_right = right
        self.panel_align_h = align

    def _set_relative_vertical_dimensions(
        self,
        top: Optional[float] = None,
        height: Optional[float] = None,
        bottom: Optional[float] = None,
        align: Optional[str] = None
    ) -> None:
        # Calculate the correct values.
        top, height, bottom, align = self._set_relative_dimenstion(
            top,
            height,
            bottom,
            align,
            align_default='middle',
            alignments=('top', 'middle', 'bottom'),
            attr_names=(
                'panel_pad_top',
                'panel_relative_height',
                'panel_pad_bottom',
            )
        )

        # Set the attributes.
        self.panel_pad_top = top
        self.panel_relative_height = height
        self.panel_pad_bottom = bottom
        self.panel_align_v = align


# Protocols.
class Frame(Panel):
    """A :class: Panel subclass that can have a frame surrounding its
    interior.
    """
    def __init__(
        self,
        frame_type: Optional[str] = None,
        frame_bg: str = '',
        frame_fg: str = '',
        *args, **kwargs
    ) -> None:
        """Initialize an instance of the class.

        For other parameters, see the documentation for :class:Panel.

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
        self.frame_type = frame_type
        self.frame_bg = frame_bg
        self.frame_fg = frame_fg

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            super().__eq__(other)
            and self.frame_type == other.frame_type
            and self.frame_bg == other.frame_bg
            and self.frame_fg == other.frame_fg
        )

    def __str__(self) -> str:
        """Return a string that will draw the entire display."""
        result = super().__str__()
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
                height=self.frame_height,
                width=self.frame_width,
                origin_y=self.frame_origin_y,
                origin_x=self.frame_origin_x,
                foreground=fg,
                background=bg
            )
        return result

    @property
    def frame_height(self) -> int:
        return super().inner_height

    @property
    def frame_width(self) -> int:
        return super().inner_width

    @property
    def frame_origin_x(self) -> int:
        return super().inner_x

    @property
    def frame_origin_y(self) -> int:
        return super().inner_y

    @property
    def inner_height(self) -> int:
        """Returns number of rows available to content within the panel."""
        height = super().inner_height
        if self.frame_type:
            height -= 2
        return height

    @property
    def inner_width(self) -> int:
        """Returns number of columns available to content within the
        panel.
        """
        width = super().inner_width
        if self.frame_type:
            width -= 2
        return width

    @property
    def inner_x(self) -> int:
        """Returns the position in the terminal of the first column
        available to content within the panel.
        """
        x = super().inner_x
        if self.frame_type:
            x += 1
        return x

    @property
    def inner_y(self) -> int:
        """Returns the position in the terminal of the first row
        available to content within the panel.
        """
        y = super().inner_y
        if self.frame_type:
            y += 1
        return y

    # Private helper methods.
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
        frame = Box(frame_type)
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


class Content(Frame):
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


class Title(Frame):
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
        y = self.frame_origin_y + self.frame_height - 1
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
            height = self.frame_height
            width = self.frame_width
            y = self.frame_origin_y
            x = self.frame_origin_x
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
        return self._title(text, self.title_align, self.frame_origin_y, frame)

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
        frame = Box(frame_type)
        bg = self.frame_bg if self.frame_bg else self.bg
        fg = self.frame_fg if self.frame_fg else self.fg
        color = self._get_color(fg, bg)
        normal = self.term.normal if color else ''
        lside = color + frame.rside + normal
        rside = color + frame.lside + normal
        return lside + title + rside
