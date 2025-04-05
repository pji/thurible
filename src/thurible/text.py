"""
text
~~~~

An object for displaying a text area in a terminal.
"""
from blessed import Terminal
from blessed.keyboard import Keystroke

from thurible.panel import Scroll, Title
from thurible.util import Box


class Text(Scroll, Title):
    """Create a new :class:`thurible.Text` object. This class displays
    text to the document and allows the user to scroll through that
    text if it is too long to fit in the terminal window. As a subclass
    of :class:`thurible.panel.Scroll` and :class:`thurible.panel.Title`,
    it can also take those parameters and has those public methods,
    properties, and active keys.

    :param content: (Optional.) The text to display in the interior
        of the panel.
    :param content_align_h: (Optional.) The horizontal alignment
        of the contents of the panel. It defaults to "left".
    :param content_align_v: (Optional.) The vertical alignment
        of the contents of the panel. It defaults to "top".
    :return: A :class:`thurible.Text` object.
    :rtype: thurible.Text
    :usage:
        To create a new minimal :class:`thurible.Text` object:

        .. testcode::

            import thurible

            text = thurible.Text()

        To create a :class:`thurible.Text` object containing the
        text "spam".:

        .. testsetup::

            import thurible

        .. testcode::

            text = thurible.Text('spam')

        Information on the sizing of :class:`thurible.Text`
        objects can be found in the :ref:`sizing` section below.
    :active keys:
        This class defines the following :ref:`active keys<active>`:

            *   KEY_END: Scroll to the end of the content.
            *   KEY_DOWN: Scroll down in the content.
            *   KEY_HOME: Scroll to the top of the content.
            *   KEY_PGDOWN: Scroll one screen down in the content.
            *   KEY_PGUP: Scroll one page up in the content.
            *   KEY_UP: Scroll one line up in the content.

    """
    # Magic methods.
    def __init__(
        self,
        content: str = '',
        content_align_h: str = 'left',
        content_align_v: str = 'top',
        *args, **kwargs
    ) -> None:
        self.content = content
        kwargs['content_align_h'] = content_align_h
        kwargs['content_align_v'] = content_align_v
        super().__init__(*args, **kwargs)

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            super().__eq__(other)
            and self.content == other.content
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
    def lines(self) -> list[str]:
        """The lines of text available to be displayed in the panel
        after they have been wrapped to fit the width of the
        interior of the panel.

        :return: A :class:`list` object containing each line of
            text as a :class:`str`.
        :rtype: list
        """
        width = self.inner_width
        if width != self._wrapped_width:
            wrapped = self.term.wrap(self.content, width)
            self._lines = wrapped
            self._wrapped_width = width
        return self._lines
