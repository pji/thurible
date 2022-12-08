"""
textdialog
~~~~~~~~~~

A text-entry dialog for terminal applications.
"""
from typing import Callable, Optional

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

        self._active_keys: dict[str, Callable] = {
            'KEY_BACKSPACE': self._delete_backwards,
            'KEY_ENTER': self._select,
            'KEY_LEFT': self._move_back,
            'KEY_RIGHT': self._move_foreward,
        }
        self._selected = 0
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
        width = self.inner_width - 2
        x = self.inner_x + 2
        y = self._align_v('bottom', 1, height) + self.inner_y

        if repr(key) in self._active_keys:
            handler = self._active_keys[repr(key)]
            data = handler(key)

        else:
            self.value += str(key)
            self._selected += 1

        if not data:
            update += self.term.move(y, x) + f'{self.value:<{width}}'
            update += self.term.reverse
            update += self.term.move(y, x + self._selected)
            if self._selected < len(self.value):
                selected_char = self.value[self._selected]
            else:
                selected_char = ' '
            update += selected_char
            update += self.term.normal

        return data, update

    # Private action handlers.
    def _delete_backwards(self, key: Optional[Keystroke]) -> str:
        """Delete the previous character."""
        self._selected -= 1
        index = self._selected
        self.value = self.value[:index] + self.value[index + 1:]
        return ''

    def _move_back(self, key: Optional[Keystroke]) -> str:
        """Move the cursor back one character."""
        self._selected -= 1
        return ''

    def _move_foreward(self, key: Optional[Keystroke]) -> str:
        """Move the cursor foreward one character."""
        self._selected += 1
        return ''

    def _select(self, key: Optional[Keystroke] = None) -> str:
        """Return the name of the selected option."""
        return self.value
