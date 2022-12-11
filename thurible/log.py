"""
log
~~~

An object for displaying a history of updating messages, such as a
log.
"""
from collections import deque
from dataclasses import dataclass
from typing import Optional, Sequence

from thurible.panel import Content, Message, Title


# Available update message.
@dataclass
class Update(Message):
    """Add a new line to the log."""
    text: str


# Class.
class Log(Content, Title):
    """Display a log of updates received from the program."""
    def __init__(
        self,
        content: Optional[Sequence[str]] = None,
        maxlen: int = 50,
        *args, **kwargs
    ) -> None:
        """Create a new :class:`thurible.Log` object. This class displays
        messages from the application in "last in first out" (LIFO)
        format. It's intended for situations were you want to provide
        the user a rolling display of status messages. As a subclass of
        :class:`thurible.panel.Content` and :class:`thurible.panel.Title`,
        it can also take those parameters and has those public methods
        and properties.

        :param content: (Optional.) A sequence of strings to display
            in the panel when it is first displayed in the terminal.
            The first item in the sequence is considered the most
            recent.
        :param maxlen: (Optional.) The total number of entries the
            :class:thurible.Log will store. This is used to allow the
            terminal window to be resized without causing the loss of
            any messages. It's not intended for the user to be able to
            scroll to view messages that have rolled off the terminal.
        :return: None.
        :rtype: NoneType
        """
        super().__init__(*args, **kwargs)
        self.maxlen = maxlen
        if content is None:
            content = deque(maxlen=self.maxlen)
        elif not isinstance(content, deque):
            d: deque[str] = deque(maxlen=self.maxlen)
            for item in content:
                d.appendleft(item)
            content = d
        self.content = content

        self._wrapped_width = -1

    def __str__(self) -> str:
        """Return a string that will draw the entire panel."""
        # Set up.
        inner_height = self.inner_height
        y = self.inner_y
        x = self.inner_x
        result = super().__str__()

        # Write the contents of the log.
        result += self._visible(
            self.lines,
            self.inner_height,
            self.inner_x,
            self.inner_y
        )
        return result

    # Properties.
    @property
    def lines(self) -> list[str]:
        """The lines of text available to be displayed in the panel
        after they have been wrapped to fit the width of the
        interior of the panel. A message from the application may
        be split into multiple lines.

        :return: A :class:list object containing each line of
            text as a :class:str.
        :rtype: list
        """
        width = self.inner_width
        if width != self._wrapped_width:
            wrapped = []
            for line in self.content:
                wrapped.extend(self.term.wrap(line, width=width))
            self._lines = wrapped
            self._wrapped_width = width
        return self._lines

    # Public methods.
    def update(self, msg: Message) -> str:
        result = super().update(msg)

        if isinstance(msg, Update):
            self.content.appendleft(msg.text)
            self._wrapped_width = -1
            result += self.clear_contents()
            result += self._visible(
                self.lines,
                self.inner_height,
                self.inner_x,
                self.inner_y
            )

        return result

    # Private helper methods.
    def _visible(
        self,
        lines: Sequence[str],
        height: int,
        x: int,
        y: int
    ) -> str:
        result = ''
        for line in lines[:height]:
            result += self.term.move(y, x) + line
            y += 1
        return result
