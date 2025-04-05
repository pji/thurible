"""
progress
~~~~~~~~

An object for announcing the progress towards a goal.
"""
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Sequence

from thurible.panel import Content, Message, Title


# Message classes.
@dataclass
class NoTick(Message):
    """Create a new :class:`thurible.progress.NoTick` object. When
    sent to :meth:`thurible.Progress.update`, this will not cause
    the progress bar to advance.

    :param message: A message to display.
    :return: A :class:`thurible.NoTick` object.
    :rtype: thurible.NoTick
    :usage:
        To create a message to advance a :class:`thurible.Progress`
        object with the text "still working...":

        .. testcode::

            import thurible

            notick = thurible.NoTick('still working...')

    """
    message: str = ''


@dataclass
class Tick(Message):
    """Create a new :class:`thurible.progress.Tick` object. When
    sent to :meth:`thurible.Progress.update`, this will cause the
    progress bar to advance.

    :param message: A message to display.
    :return: A :class:`thurible.Tick` object.
    :rtype: thurible.Tick
    :usage:
        To create a message to advance a :class:`thurible.Progress`
        object with the text "another step completed":

        .. testcode::

            import thurible

            tick = thurible.Tick('another step completed')

    """
    message: str = ''


# Panel class.
class Progress(Content, Title):
    """Create a new :class:`thurible.Progress` object. This
    object displays a bar representing how much progress has
    been achieved towards a goal. As a subclass of
    :class:`thurible.panel.Content` and :class:`thurible.panel.Title`,
    it can also take those parameters and has those public methods
    and properties.

    :param steps: The number of steps required to achieve the
        goal.
    :param progress: (Optional.) The number of steps that have been
        completed.
    :param bar_bg: (Optional.) A string describing the background
        color of the bar. See the documentation for :mod:`blessed`
        for more detail on the available options.
    :param bar_fg: (Optional.) A string describing the foreground
        color of the bar. See the documentation for :mod:`blessed`
        for more detail on the available options.
    :param max_messages: (Optional.) How many status messages should
        be stored to be displayed.
    :param messages: (Optional.) Any status messages to start in the
        display. Since new messages are added to the display at the
        top, the messages passed in this sequence should be stored
        in reverse chronological order.
    :param timestamp: (Optional.) Add a timestamp to the messages
        when they are displayed.
    :return: A :class:`thurible.Progress` object.
    :rtype: thurible.Progress
    :usage:
        To create a :class:`thurible.Progress` object with six steps:

        .. testcode::

            import thurible

            progress = thurible.Progress(6)

        To send an update message to a :class:`thurible.Progress`
        object that advances the bar use a :class:`thurible.Tick`
        message:

        .. testsetup:: progress

            import thurible
            progress = thurible.Progress(6)

        .. testcode:: progress

            tick = thurible.Tick('First step complete.')
            progress.update(tick)

        To send an update message to a :class:`thurible.Progress`
        object that does not advance the bar use a :class:`thurible.NoTick`
        message:

        .. testcode:: progress

            notick = thurible.NoTick('A thing happened.')
            progress.update(notick)

        Information on the sizing of :class:`thurible.Progress`
        objects can be found in the :ref:`sizing` section below.

    """
    def __init__(
        self,
        steps: int,
        progress: int = 0,
        bar_bg: str = '',
        bar_fg: str = '',
        max_messages: int = 0,
        messages: Optional[Sequence[str]] = None,
        timestamp: bool = False,
        *args, **kwargs
    ) -> None:
        self._notick = False
        self._t0 = datetime.now()
        self._wrapped_width = -1

        self.steps = steps
        self.progress = progress
        self.bar_bg = bar_bg
        self.bar_fg = bar_fg
        self.max_messages = max_messages
        self.timestamp = timestamp
        self.messages: deque = deque(maxlen=self.max_messages)
        if messages:
            for msg in messages:
                self._add_message(msg)
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        """Return a string that will draw the entire panel."""
        # Set up.
        result = super().__str__()
        height = 1 + self.max_messages
        y = self._align_v('middle', height, self.inner_height) + self.inner_y
        x = self.content_x

        # Add the progress bar.
        result += self.term.move(y, x) + self.progress_bar
        y += 1

        # Add messages.
        if self.max_messages:
            result += self._visible_messages(x, y)

        # Return the resulting string.
        return result

    # Properties.
    @property
    def lines(self) -> list[str]:
        """The lines of text available to be displayed in the panel
        after they have been wrapped to fit the width of the
        interior of the panel. A message from the application may
        be split into multiple lines.

        :return: A :class:`list` object containing each line of
            text as a :class:`str`.
        :rtype: list
        """
        width = self.content_width
        if width != self._wrapped_width:
            wrapped = []
            for line in self.messages:
                wrapped.extend(self.term.wrap(line, width=width))
            self._lines = wrapped
            self._wrapped_width = width
        return self._lines

    @property
    def progress_bar(self) -> str:
        """The progress bar as a string.

        :return: A :class:`str` object.
        :rtype: str
        """
        # Color the bar.
        result = self._get_color(self.bar_fg, self.bar_bg)

        # Unicode has characters to fill eighths of a character,
        # so we can resolve progress at eight times the width available
        # to us.
        notches = self.content_width * 8

        # Determine the number of notches filled.
        notches_per_step = notches / self.steps
        progress_notches = notches_per_step * self.progress
        full = int(progress_notches // 8)
        part = int(progress_notches % 8)

        # The Unicode characters we are using are the block fill
        # characters in the range 0x2588–0x258F. This takes
        # advantage of the fact they are in order to make it
        # easier to find the one we need.
        blocks = {i: chr(0x2590 - i) for i in range(1, 9)}

        # Build the bar.
        progress = blocks[8] * full
        if part:
            progress += blocks[part]
        result += f'{progress:<{self.content_width}}'

        # If a color was set, return to normal to avoid unexpected
        # behavior. Then return the string.
        if self.bar_bg or self.bar_fg:
            result += self.term.normal
        return result

    # Public methods.
    def update(self, msg: Message) -> str:
        """Act on a message sent by the application.

        :class:`thurible.Progress` responds to the following
        update messages:

        *   :class:`thurible.progress.Tick`: Advance the progress bar
            and display any message passed.
        *   :class:`thurible.progress.NoTick`: Do not advance the
            progress bar but display the message passed as a
            temporary message. The temporary message will be replaced
            by the next message received.

        :param msg: A message sent by the application.
        :return: A :class:`str` object containing any updates needed to
            be made to the terminal display.
        :rtype: str
        """
        result = ''

        # If a tick is received, advance the progress bar.
        if isinstance(msg, Tick):
            if self._notick and self.max_messages:
                self.messages.popleft()
            self._notick = False
            self.progress += 1
            if self.max_messages:
                self._add_message(msg.message)
                self._wrapped_width = -1
            result += self._make_display()

        # If a notick is received, update the status messages but
        # don't advance the progress bar.
        elif isinstance(msg, NoTick) and self.max_messages:
            if self._notick:
                self.messages.popleft()
            self._notick = True
            self._add_message(msg.message)
            self._wrapped_width = -1
            result += self._make_display()

        return result

    # Private helper methods.
    def _add_message(self, msg) -> None:
        if self.timestamp:
            stamp = datetime.now() - self._t0
            mins = stamp.seconds // 60
            secs = int(stamp.seconds % 60)
            msg = f'{mins:0>2}:{secs:0>2} {msg}'
        self.messages.appendleft(msg)

    def _make_display(self) -> str:
        result = ''
        height = 1 + self.max_messages
        y = self.inner_y
        y += self._align_v('middle', height, self.inner_height)
        x = self.content_x
        result += self.term.move(y, x) + self.progress_bar
        y += 1

        if self.max_messages:
            result += self._visible_messages(x, y)

        return result

    def _visible_messages(self, x: int, y: int) -> str:
        result = ''
        width = self.content_width
        for i, line in zip(range(self.max_messages), self.lines):
            result += f'{self.term.move(y + i, x)}{line:<{width}}'
        return result
