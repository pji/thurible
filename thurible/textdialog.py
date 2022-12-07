"""
textdialog
~~~~~~~~~~

A text-entry dialog for terminal applications.
"""
from typing import Optional

from blessed.keyboard import Keystroke

from thurible.panel import Content, Title


# Class.
class TextDialog(Content, Title):
    """A text-entry dialog for terminal applications."""
    def __init__(
        self,
        message_text: str,
        *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.message_text = message_text

        self._active_keys = {
            'KEY_ENTER': self._select,
        }
        self.value = ''

    def __str__(self) -> str:
        result = super().__str__()

        result += self.message

        height = self.inner_height
        x = self.inner_x
        y = self._align_v('bottom', 1, height) + self.inner_y
        result += self.term.move(y, x) + '>'

        x += 2
        result += self.term.reverse
        result += self.term.move(y, x) + ' '
        result += self.term.normal

        return result

    # Properties
    @property
    def message(self) -> str:
        wrapped = self.term.wrap(self.message_text, width=self.inner_width)
        length = len(wrapped)
        y = self._align_v('middle', length, self.inner_height) + self.inner_y
        x = self.inner_x
        result = f'{self.term.move(y, x)}{self.message_text}'
        return result

    # Public methods.
    def action(self, key: Keystroke) -> tuple[str, str]:
        # These are the results that are returned.
        data = ''
        update = ''

        height = self.inner_height
        x = self.inner_x + 2 + len(self.value)
        y = self._align_v('bottom', 1, height) + self.inner_y

        if repr(key) in self._active_keys:
            handler = self._active_keys[repr(key)]
            data = handler(key)

        else:
            self.value += str(key)
            update += self.term.move(y, x) + str(key)
            update += self.term.reverse
            update += ' '
            update += self.term.normal

        return data, update

    # Private action handlers.
    def _select(self, key: Optional[Keystroke] = None) -> str:
        """Return the name of the selected option."""
        return self.value
