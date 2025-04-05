"""
text
~~~~

An object for displaying a data table in a terminal.
"""
from __future__ import annotations

import unicodedata as ucd
from dataclasses import astuple, dataclass, fields
from typing import TYPE_CHECKING, Any, Optional, Protocol, Sequence

from thurible.panel import Scroll, Title
from thurible.util import Box as Frame


if TYPE_CHECKING:
    from _typeshed import DataclassInstance


# Classes.
class Table(Scroll, Title):
    """Create a new :class:`thurible.Table` object. This class displays
    a table of data to the user. As a subclass of
    :class:`thurible.panel.Scroll` and :class:`thurible.panel.Title`,
    it can also take those parameters and has those public methods,
    properties, and active keys.

    :param records: A sequence of dataclasses that will be displayed
        within the panel. The data held by the dataclass can be of
        any type, but it must be able to be coerced into a :class:str.
    :param inner_frame: (Optional.) Whether there should be a visible
        frame around each cell in the panel.
    :param content_align_h: (Optional.) The horizontal alignment
        of the contents of the panel. It defaults to "left".
    :param content_align_v: (Optional.) The vertical alignment
        of the contents of the panel. It defaults to "top".
    :return: A :class:`thurible.Table` object.
    :rtype: thurible.Table
    :usage:
        To create a new :class:`thurible.Table` object:

        .. testcode::

            from dataclasses import dataclass
            import thurible

            @dataclass
            class Record:
                name: str
                count: int

            record_1 = Record('Graham', 1)
            record_2 = Record('Michael', 2)
            record_3 = Record('John', 3)
            records = [record_1, record_2, record_3,]
            table = thurible.Table(records)

        Information on the sizing of :class:`thurible.Table`
        objects can be found in the :ref:`sizing` section below.

    """
    def __init__(
        self,
        records: Sequence[DataclassInstance],
        inner_frame: bool = False,
        content_align_h: str = 'left',
        content_align_v: str = 'top',
        *args, **kwargs
    ) -> None:
        self.records = records
        self.inner_frame = inner_frame
        kwargs['content_align_h'] = content_align_h
        kwargs['content_align_v'] = content_align_v
        super().__init__(*args, **kwargs)

        self._char_true = '█'
        self._char_false = '▁'

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            super().__eq__(other)
            and self.records == other.records
            and self.inner_frame == other.inner_frame
            and self._char_true == other._char_true
            and self._char_false == other._char_false
            and self._ofr == other._ofr
        )

    def __str__(self) -> str:
        """Return a string that will draw the entire panel."""
        # Set up.
        lines = self.lines
        length = len(lines)
        height = self.inner_height
        width = self.inner_width
        y = self.inner_y
        x = self.inner_x
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
    def field_names(self) -> list[str]:
        """The names of each field of data contained within the records
        being displayed.

        :return: A :class:`list` object containing each name as
            a :class:`str` object.
        :rtype: list
        """
        if '_field_names' not in self.__dict__:
            self._field_names = [f.name for f in fields(self.records[0])]
        return self._field_names

    @property
    def field_widths(self) -> list[int]:
        """The width in characters of each field in the table, as
        determined by the longest value for this field found in
        the dataclasses.

        :return: A :class:`list` object containing each width as an
            :class:`int`.
        :rtype: list

        """
        if '_field_widths' not in self.__dict__:
            fnames = self.field_names
            fwidths = self._calc_field_widths(self.records, fnames)
            if sum(fwidths) + len(fwidths) - 1 > self.inner_width:
                fwidths = self._calc_field_widths_overflow(fwidths)
            self._field_widths = fwidths
        return self._field_widths

    @property
    def lines(self) -> list[str]:
        """The lines of text available to be displayed in the panel
        after they have been wrapped to fit the width of the
        interior of the panel.

        :return: A :class:`list` object containing each line of
            text as a :class:`str`.
        :rtype: list
        """
        lines = []

        align = '<'
        if self.content_align_h == 'center':
            align = '^'
        elif self.content_align_h == 'right':
            align = '>'
        width = self.inner_width
        fnames = self.field_names
        fwidths = self.field_widths
        if self.frame_type:
            frame = Frame(self.frame_type)

        for record in self.records:
            line = ''
            seperator = ' '
            if self.inner_frame and self.frame_type:
                seperator = frame.mver
            for fname, fwidth in zip(fnames, fwidths):
                line += self._get_field_value(record, fname, fwidth)
                if fname != fnames[-1]:
                    line += seperator
            line = f'{line:{align}{width}}'
            if self.frame_type:
                line = frame.mver + line + frame.mver
            lines.append(line)

            if self.inner_frame and self.frame_type:
                line = ''
                seperator = frame.mid
                for fname, fwidth in zip(fnames, fwidths):
                    line += frame.mhor * fwidth
                    if fname != fnames[-1]:
                        line += seperator
                line = f'{line:{frame.mhor}{align}{width}}'
                line = frame.lside + line + frame.rside
                lines.append(line)

        if self.inner_frame and self.frame_type:
            lines = lines[:-1]
        return lines

    # Private helper methods.
    def _calc_field_widths(
        self,
        records: Sequence[DataclassInstance],
        names: list[str],
    ) -> list[int]:
        result = []
        for name in names:
            data = [getattr(record, name) for record in records]
            width = 1
            if not isinstance(data[0], bool):
                width = self._calc_max_width(data)
            result.append(width)
        return result

    def _calc_field_widths_overflow(self, fwidths: list[int]) -> list[int]:
        # We don't want to affect the small fields, so calculate the
        # size of an average field to use to determine which fields are
        # small.
        num_fields = len(fwidths)
        divs = num_fields - 1
        avail = self.inner_width - divs
        avg_fwidth = avail // num_fields

        # Determine which fields are big.
        big_mask = [w > avg_fwidth for w in fwidths]

        # Determine the new field size for the big fields.
        big_avail = avail - sum(w for w in fwidths if w <= avg_fwidth)
        num_big = len([item for item in big_mask if item])
        big_avg = big_avail // num_big

        # Set the big fields to their new sizes.
        result = fwidths[:]
        for i in range(num_fields):
            if big_mask[i]:
                result[i] = big_avg

        # Add back in any extra space left over from using floor division
        # to calculate the new big field size.
        remain = big_avail % num_big
        bigs = [i for i, v in enumerate(big_mask) if v]
        for i in bigs[:remain]:
            result[i] += 1

        # Return the result.
        return result

    def _calc_max_width(self, data: Sequence[Any]) -> int:
        """Determine the length of the longest string."""
        strings = (str(datum) for datum in data)
        return max(len(s) for s in strings)

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
        result = super()._frame(
            frame_type,
            height,
            width,
            origin_y,
            origin_x,
            foreground,
            background
        )
        result += self._get_color(foreground, background)

        if self.inner_frame and self.frame_type:
            fwidths = self.field_widths[:-1]
            x = origin_x + 1
            bottom_y = origin_y + height - 1
            for fwidth in fwidths:
                x += fwidth
                result += self.term.move(origin_y, x) + frame.mtop
                result += self.term.move(bottom_y, x) + frame.mbot
                x += 1

        if background or foreground:
            result += self.term.normal
        return result

    def _get_field_value(
        self,
        record: DataclassInstance,
        field: str,
        width: int
    ) -> str:
        align = '<'
        value = getattr(record, field)

        if isinstance(value, bool) and value:
            value = self._char_true
        elif isinstance(value, bool):
            value = self._char_false
        elif value and isinstance(value, int):
            align = '>'

        value = str(value)
        if len(value) > width:
            value = value[:width - 3] + self._ofr

        for i, char in enumerate(value):
            if ucd.category(char) == 'Cc':
                value = value[0:i] + ' ' + value[i + 1:]

        return f'{value:{align}{width}}'

    def _visible(self, lines: list[str], width: int, y: int, x: int) -> str:
        """Output the lines in the display."""
        update = ''
        update += self._get_color(self.fg, self.bg)
        for i, line in enumerate(lines[self._start: self._stop]):
            x_mod = self._align_h(self.content_align_h, len(line), width)
            if self.frame_type:
                x_mod -= 1
            update += self.term.move(y + i, x + x_mod) + line
        if self.fg or self.bg:
            update += self.term.normal
        return update
