"""
progress
~~~~~~~~

An object for announcing the progress towards a goal.
"""
from thurible.panel import Content, Message, Title


# Message class.
class Tick(Message):
    """Create a new :class:`thurible.progress.Tick` object.

    :return: None.
    :rtype: NoneType
    """


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
    :return: None.
    :rtype: NoneType
    """
    def __init__(
        self,
        steps: int,
        progress: int = 0,
        bar_bg: str = '',
        bar_fg: str = '',
        *args, **kwargs
    ) -> None:
        self.steps = steps
        self.progress = progress
        self.bar_bg = bar_bg
        self.bar_fg = bar_fg
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        """Return a string that will draw the entire panel."""
        # Set up.
        result = super().__str__()
        y = self._align_v('middle', 1, self.inner_height) + self.inner_y
        x = self.content_x

        # Add the progress bar.
        result += self.term.move(y, x) + self.progress_bar

        # Return the resulting string.
        return result

    # Properties.
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

        :param msg: A message sent by the application.
        :return: A :class:`str` object containing any updates needed to
            be made to the terminal display.
        :rtype: str
        """
        result = ''
        if isinstance(msg, Tick):
            self.progress += 1
            y = self._align_v('middle', 1, self.inner_height) + self.inner_y
            x = self.content_x
            result += self.term.move(y, x) + self.progress_bar
        return result
