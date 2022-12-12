"""
progress
~~~~~~~~

An object for announcing the progress towards a goal.
"""
from thurible.panel import Content, Message, Title


# Class.
class Progress(Content, Title):
    def __init__(
        self,
        steps: int,
        progress: int = 0,
        *args, **kwargs
    ) -> None:
        """Create a new :class:`thurible.Progress` object. This
        object displays a bar representing how much progress has
        been achieved towards a goal. As a subclass of
        :class:`thurible.panel.Content` and :class:`thurible.panel.Title`,
        it can also take those parameters and has those public methods
        and properties.

        :param steps: The number of steps required to achieve the
            goal.
        :param progress: The number of steps that have been completed.
        :return: None.
        :rtype: NoneType
        """
        self.steps = steps
        self.progress = progress
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        """Return a string that will draw the entire panel."""
        # Set up.
        result = super().__str__()
        width = self.inner_width
        y = self._align_v('middle', 1, self.inner_height)
        x = self.inner_x

        # Add the progress bar.
        notches = width * 8
        notches_per_step = notches / self.steps
        progress_notches = notches_per_step * self.progress
        full = int(progress_notches // 8)
        part = int(progress_notches % 8)
        blocks = {i: chr(0x2590 - i) for i in range(1, 9)}
        progress = blocks[8] * full
        if part:
            progress += blocks[part]
        result += self.term.move(y, x) + f'{progress:<{width}}'

        # Return the resulting string.
        return result
