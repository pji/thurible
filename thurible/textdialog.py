"""
textdialog
~~~~~~~~~~

A text-entry dialog for terminal applications.
"""
from typing import Callable, Optional
from unicodedata import category

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
            'KEY_DELETE': self._delete,
            'KEY_END': self._end,
            'KEY_HOME': self._home,
            'KEY_ENTER': self._select,
            'KEY_LEFT': self._move_back,
            'KEY_RIGHT': self._move_foreward,
        }
        self._selected = 0
        self.prompt = '> '
        self.value = ''

    def __str__(self) -> str:
        result = super().__str__()

        result += self.message

        height = self.inner_height
        x = self.inner_x
        y = self._align_v('bottom', 1, height) + self.inner_y
        result += self.term.move(y, x) + self.prompt

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
        # If, somehow, we received something that isn't a keystroke,
        # something has gone seriously wrong.
        if not isinstance(key, Keystroke):
            cls_name = type(key).__name__
            msg = f'Can only accept Keystrokes. Received: {cls_name}.'
            raise ValueError(msg)

        # These are the results that are returned.
        data = ''
        update = ''

        # Handle the keys with defined behavior.
        if repr(key) in self._active_keys:
            handler = self._active_keys[repr(key)]
            data = handler(key)

        # If it's non-printable and has no defined behavior, pass it
        # back to the program to figure out.
        elif key.is_sequence or category(str(key)) == 'Cc':
            data = str(key)

        # If it's printable and the cursor is in the middle of the
        # text being typed, insert the character in front of the
        # current position.
        elif self._selected < len(self.value):
            index = self._selected
            self.value = (self.value[0:index] + str(key) + self.value[index:])
            self._selected += 1

        # Otherwise, add it to the end of the text being typed.
        else:
            self.value += str(key)
            self._selected += 1

        # If data isn't being returned, we probably need to update the
        # terminal to show what happened.
        if not data:
            # Set up.
            prompt_length = len(self.prompt)
            height = self.inner_height
            width = self.inner_width - prompt_length
            x = self.inner_x + prompt_length
            y = self._align_v('bottom', 1, height) + self.inner_y

            # Create the string used to update the terminal.
            update += self.term.move(y, x) + f'{self.value:<{width}}'
            update += self.term.reverse
            update += self.term.move(y, x + self._selected)
            if self._selected < len(self.value):
                selected_char = self.value[self._selected]
            else:
                selected_char = ' '
            update += selected_char
            update += self.term.normal

        # Return the results as a tuple.
        return data, update

    # Private action handlers.
    def _delete(self, key: Optional[Keystroke]) -> str:
        """Delete the selected character."""
        index = self._selected
        self.value = self.value[:index] + self.value[index + 1:]
        return ''

    def _delete_backwards(self, key: Optional[Keystroke]) -> str:
        """Delete the previous character."""
        self._selected -= 1
        return self._delete(key)

    def _end(self, key: Optional[Keystroke]) -> str:
        """Move the cursor to the last position."""
        self._selected = len(self.value)
        return ''

    def _home(self, key: Optional[Keystroke]) -> str:
        """Move the cursor to the first character."""
        self._selected = 0
        return ''

    def _move_back(self, key: Optional[Keystroke]) -> str:
        """Move the cursor back one character."""
        if self._selected > 0:
            self._selected -= 1
        return ''

    def _move_foreward(self, key: Optional[Keystroke]) -> str:
        """Move the cursor foreward one character."""
        if self._selected < len(self.value):
            self._selected += 1
        return ''

    def _select(self, key: Optional[Keystroke] = None) -> str:
        """Return the name of the selected option."""
        return self.value
