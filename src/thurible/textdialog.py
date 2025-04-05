"""
textdialog
~~~~~~~~~~

A text-entry dialog for terminal applications.
"""
from typing import Callable, Optional
from unicodedata import category

from blessed.keyboard import Keystroke

from thurible.dialog import Dialog
from thurible.panel import Content, Title


# Class.
class TextDialog(Content, Title):
    """Create a new :class:`thurible.TextDialog` object. This class
    displays a message to the user and allows them to input a string,
    which is send to the application. As a subclass of
    :class:`thurible.panel.Content` and :class:`thurible.panel.Title`,
    it can also take those parameters and has those public methods,
    properties, and active keys.

    :param message_text: The text of the prompt to be displayed to
        the user.
    :return: A :class:`thurible.TextDialog` object.
    :rtype: thurible.Text
    :usage:
        To create a :class:`thurible.TextDialog` object containing the
        text "spam".:

        .. testcode::

            import thurible

            text = thurible.TextDialog('spam')

        Information on the sizing of :class:`thurible.TextDialog`
        objects can be found in the :ref:`sizing` section below.
    :active keys:
        This class defines the following active keys:

            *   KEY_BACKSPACE: Delete the previous character.
            *   KEY_DELETE: Delete the next character.
            *   KEY_END: Move the cursor to after the last character.
            *   KEY_HOME: Move the cursor to the first character.
            *   KEY_ENTER: Finish text entry and send input to the
                application.
            *   KEY_LEFT: Move the cursor to the next character.
            *   KEY_RIGHT: Move the cursor to the previous character.

        While not registered as active keys, all other key presses that
        do not result in key sequences as defined by :mod:`blessed` or
        control characters as defined by the Unicode specification are
        intercepted by the panel. The :class:`str` value of that key
        press is inserted into the text field at the position of the
        cursor.

        For more information on active keys, see :ref:`active`.

    """
    def __init__(
        self,
        message_text: str,
        *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.message_text = message_text

        self.register_key('KEY_BACKSPACE', self._delete_backwards)
        self.register_key('KEY_DELETE', self._delete)
        self.register_key('KEY_END', self._end)
        self.register_key('KEY_HOME', self._home)
        self.register_key('KEY_ENTER', self._select)
        self.register_key('KEY_LEFT', self._move_back)
        self.register_key('KEY_RIGHT', self._move_foreward)

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
        result = ''
        for i, line in enumerate(wrapped):
            result += f'{self.term.move(y + i, x)}{line}'
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
