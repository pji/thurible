"""
dialog
~~~~~~

A dialog for terminal applications.
"""
from typing import Optional, Sequence

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
    """Create a new :class:`thurible.Dialog` object. This class displays
    a message to the user and offers pre-defined options for the
    user to chose from. As a subclass of :class:`thurible.panel.Content`
    and :class:`thurible.panel.Title`, it can also take those parameters
    and has those public methods and properties.

    :param message_text: The text of the prompt to be displayed to
        the user.
    :param options: The options the user can chose from. This is a
        sequence of :class:`thurible.Option` objects.
    :return: A :class:`Dialog` object.
    :rtype: thurible.Dialog
    :usage:
        To create a new :class:`thurible.Dialog` object with the
        message text `spam` and default yes/no options:

        .. testcode::

            import thurible

            dialog = thurible.Dialog('spam')

        Information on the sizing of :class:`thurible.Dialog`
        objects can be found in the :ref:`sizing` section below.
    :active keys:
        This class defines the following :ref:`active keys<active>`:

            *   KEY_ENTER: Select current option.
            *   KEY_LEFT: Move to next option.
            *   KEY_RIGHT: Move to previous option.
            *   <hotkey>: Move to the defined option.

    """
    def __init__(
        self,
        message_text: str,
        options: Sequence[Option] = yes_no,
        *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.message_text = message_text
        self.options = options

        # Defined action keys.
        self.register_key('KEY_ENTER', self._select)
        self.register_key('KEY_LEFT', self._select_left)
        self.register_key('KEY_RIGHT', self._select_right)
        for option in self.options:
            hotkey = f"'{option.hotkey}'"
            self.register_key(hotkey, self._hotkey)
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
        """
        The message as a string that could be used to update the terminal.

        :return: A :class:`str` object.
        :rtype: str
        """
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
        """Act on a keystroke typed by the user.

        :param key: A :class:`blessed.keyboard.Keystroke` object representing
            the key pressed by the user.
        :return: A :class:`tuple` object containing two :class:`str` objects.
            The first string is any data that needs to be sent to the
            application. The second string contains any updates needed
            to be made to the terminal display.
        :rtype: tuple
        """
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
