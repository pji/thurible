"""
splash
~~~~~~

A splash screen for terminal applications.
"""
from blessed import Terminal

from thurible.panel import Content, Title


class Splash(Content, Title):
    """A splash screen for terminal applications."""
    # Magic methods.
    def __init__(
        self,
        content: str = '',
        *args, **kwargs
    ) -> None:
        """Create a new :class:`thurible.Splash` object. This class
        creates a splash screen that can be displayed in the terminal.
        As a subclass of :class:`thurible.panel.Content` and
        :class:`thurible.panel.Title`, it can also take those parameters
        and has those public methods and properties.

        :param content: (Optional.) The text to display within the
            interior of the panel.
        :return: None.
        :rtype: NoneType
        """
        self.content = content
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        """Return a string that will draw the entire panel."""
        # Set up.
        lines = self.lines
        height = self.inner_height
        width = self.inner_width
        y = self.inner_y
        x = self.inner_x
        result = super().__str__()

        length_v = len(lines)
        y += self._align_v(self.content_align_v, length_v, height)

        for i, line in enumerate(lines):
            length_h = len(line)
            x_mod = self._align_h(self.content_align_h, length_h, width)
            result += self.term.move(y + i, x + x_mod) + line
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
        return self.content.split('\n')
