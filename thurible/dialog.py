"""
dialog
~~~~~~

A dialog for terminal applications.
"""
from typing import Sequence, Optional

from blessed.keyboard import Keystroke

from thurible.menu import Option
from thurible.panel import Content, Title


# Common dialog options.
cont = (Option('Continue', ''),)
yes_no = (
    Option('Yes', 'y'),
    Option('No', 'n'),
)


# Classes.
class Dialog(Content, Title):
    """A simple dialog for terminal applications."""
    def __init__(
        self,
        message_text: str,
        options: Sequence[Option] = yes_no,
        *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.message_text = message_text
        self.options = options

        self._active_keys = {
            'KEY_ENTER': self._select,
            'KEY_LEFT': self._select_left,
            'KEY_RIGHT': self._select_right,
        }
        for option in self.options:
            hotkey = f"'{option.hotkey}'"
            self._active_keys[hotkey] = self._hotkey
        self._selected = len(self.options) - 1

    def __str__(self) -> str:
        result = super().__str__()

        result += self.message

        height = self.inner_height
        width = self.inner_width
        y = self._align_v('bottom', 1, height) + self.inner_y
        for i, option in enumerate(self.options[::-1]):
            opt_text = ''
            if i == len(self.options) - 1 - self._selected:
                opt_text += self.term.reverse
            name = option.name
            length = len(name) + 2
            x = self._align_h('right', length, width) + self.inner_x
            opt_text += f'{self.term.move(y, x)}[{name}]'
            if i == len(self.options) - 1 - self._selected:
                opt_text += self.term.normal
            result += opt_text
            width -= length + 1

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

        if repr(key) in self._active_keys:
            handler = self._active_keys[repr(key)]
            data = handler(key)
        else:
            data = str(key)

        if not data:
            height = self.inner_height
            width = self.inner_width
            y = self._align_v('bottom', 1, height)
            for i, option in enumerate(self.options[::-1]):
                opt_text = ''
                if i == len(self.options) - 1 - self._selected:
                    opt_text += self.term.reverse
                name = option.name
                length = len(name) + 2
                x = self._align_h('right', length, width)
                opt_text += f'{self.term.move(y, x)}[{name}]'
                if i == len(self.options) - 1 - self._selected:
                    opt_text += self.term.normal
                update += opt_text
                width -= length + 1

        return data, update

    # Private action handlers.
    def _hotkey(self, key: Optional[Keystroke] = None) -> str:
        """Select the option assigned to the hot key."""
        hotkeys = [option.hotkey for option in self.options]
        self._selected = hotkeys.index(str(key))
        return ''

    def _select(self, key: Optional[Keystroke] = None) -> str:
        """Return the name of the selected option."""
        return self.options[self._selected].name

    def _select_left(self, key: Optional[Keystroke] = None) -> str:
        """Select the next option to the left."""
        if self._selected > 0:
            self._selected -= 1
        return ''

    def _select_right(self, key: Optional[Keystroke] = None) -> str:
        """Select the next option to the right."""
        if self._selected < len(self.options) - 1:
            self._selected += 1
        return ''
