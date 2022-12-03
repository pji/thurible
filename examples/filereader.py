"""
filereader
~~~~~~~~~~

Browse to and open files as either text or binary data.
"""
from argparse import ArgumentParser
import unicodedata as ucd
from dataclasses import dataclass
from pathlib import Path
from queue import Queue
from threading import Thread
from typing import Optional, Sequence

import thurible as thb
from thurible import messages as tm
from thurible.dialog import cont


# Classes.
class FileReaderMenu(thb.Menu):
    """A menu that tracks whether a entry was selected with a `b` or
    the enter key.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._active_keys["'b'"] = self._enter_with_mode
        self._active_keys['KEY_ENTER'] = self._enter_with_mode

    def _enter_with_mode(self, key: Optional[thb.Keystroke] = None) -> str:
        """Send the key pressed and the selected option back to the
        program.
        """
        resp = self._select(key)

        # Since we are using the record separator as a delimiter, we
        # have to make sure the user isn't passing a record separator
        # in to break things. So, we're going to check for that
        # character and neutralize it to a newline.
        key_str = str(key)
        if key_str == '\x1e':
            key_str = '\n'

        # Ideally, this would return a tuple with two values: the
        # string for the Keystroke and the name of the option. But,
        # action handlers has to return a string. Therefore, both the
        # Keystroke and the option name are passed in the string,
        # separated by the record separator.
        return key_str + '\x1e' + resp


@dataclass
class Qword:
    """A row for a table that contains a hexdump-like representation of
    a qword (eight bytes) of binary data.
    """
    position: str = ''
    b0: str = ''
    b1: str = ''
    b2: str = ''
    b3: str = ''
    b4: str = ''
    b5: str = ''
    b6: str = ''
    b7: str = ''
    in_latin: str = ''


# Functions.
def build_names_list(
    paths: list[str],
    prefix: str = ' ',
    show_hidden: bool = False
) -> list[str]:
    """Turn a list of paths into a list of file or directory names
    prefixed with the given indicator.
    """
    names = [path.name for path in paths]
    if not show_hidden:
        names = [name for name in names if not name.startswith('.')]
    names = sorted(names)
    return [f'{prefix} {name}' for name in names]


def create_binary_table(path: str | Path) -> thb.Table:
    """Return a table with the hexdump of the given file.

    :param path: The path to the file to open.
    :return: A :class:thurible.Table object containing the binary
        data from the given file.
    :rtype: thurible.Table
    """
    # Ensure we are working with a pathlib.Path object since some tests
    # may still be sending strings.
    if not isinstance(path, Path):
        path = Path(path)

    # Get the contents of the file as a binary string.
    data = read_file_as_binary(path)

    # Get the rows for the table that will be displayed in the terminal.
    # Each row is represented by a dataclass, in this case Qword. Every
    # row for the table needs to be the same type of data class because
    # Table parses the rows by the names of the attributes of the first
    # row.
    qwords = get_hex(data)

    # Create and return the thurible.Table object containing the
    # binary data in a hexdump-like format.
    return thb.Table(
        records=qwords,
        footer_text='\u241b:Back q:Quit',
        footer_frame=True,
        title_text=str(path),
        title_frame=True,
        frame_type='heavy'
    )


def create_dir_menu(
    path: str | Path = '',
    show_hidden: bool = False
) -> FileReaderMenu:
    """Return a menu containing the contents of the given directory."""
    # If no path was given, default to the current working directory.
    if not path:
        path = Path().cwd()

    # Ensure we are working with a pathlib.Path object since some tests
    # may still be sending strings.
    elif not isinstance(path, Path):
        path = Path(path)

    # Get the list of files and directories in the directory at the
    # given path.
    contents = get_dir_list(path)

    # Turn those files and directories into a list of Option objects
    # that will become the selectable optons in the menu.
    options = create_options_from_paths(contents, show_hidden)

    # Create and return a FileReadrMenu object with the list of files
    # and directories as selectable options.
    return FileReaderMenu(
        options=options,
        footer_text='⏎:Text b:Bin q:Quit',
        footer_frame=True,
        title_text=str(path),
        title_frame=True,
        frame_type='double'
    )


def create_options_from_paths(
    paths: Sequence[str | Path],
    show_hidden: bool = False
) -> list[thb.Option]:
    """Return the file paths as a list of options.

    :param paths: The paths that will be options in the menu.
    :param show_hidden: (Optional.) Whether the hidden files are
        shown in the menu.
    :return: A :class:list of :class:thurible.Option objects.
    :rtype: list
    """
    # Ensure we are working with pathlib.Path objects since some tests
    # may still be sending strings.
    paths = [Path(path) for path in paths]

    # Split the paths into directories and files so they can be
    # labelled differently in the menu.
    dirs = [path for path in paths if path.is_dir()]
    files = [path for path in paths if not path.is_dir()]

    # Start the menus with the option to go back to the parent
    # directory.
    names = ['▸ ..',]

    # Label the directories differently from the files, so it's clear
    # which is which in the menu.
    names += build_names_list(dirs, '▸', show_hidden)
    names += build_names_list(files, ' ', show_hidden)

    # Create the menu options and return them.
    return [thb.Option(name, '') for name in names]


def create_text(path: str | Path) -> thb.Text:
    """Return a text reader with the contents of the given file.

    :param path: The file to read.
    :return: A :class:thurible.Text containing the text from the
        file.
    :rtype: thurible.Text
    """
    # Ensure we are working with a pathlib.Path object since some tests
    # may still be sending strings.
    if not isinstance(path, Path):
        path = Path(path)

    # Get the text from the file. Default to interpreting the test as
    # UTF-8. If that fails, use Latin-1, which will work. This will
    # misinterpret files that aren't in those character sets. There
    # should probably an option to select the character set manually
    # in the future.
    try:
        content = read_file_as_text(path, 'utf_8')
    except UnicodeDecodeError:
        content = read_file_as_text(path, 'latin_1')

    # Create and return a thurible.Text object for reading the text
    # in the given file.
    return thb.Text(
        content=content,
        footer_text='\u241b:Back q:Quit',
        footer_frame=True,
        title_text=str(path),
        title_frame=True,
        frame_type='heavy'
    )


def get_dir_list(path: str | Path) -> list[Path]:
    """Return the contents of the directory at the given path."""
    # Ensure we are working with a pathlib.Path object since some tests
    # may still be sending strings.
    if isinstance(path, str):
        path = Path(path)

    # Get and return the list of directories and files in the given
    # directory.
    children = [child for child in path.iterdir()]
    return children


def get_hex(data: bytes) -> list[Qword]:
    """Turn data from a binary file into records for displaying as a
    hexdump.

    :param data: Binary data.
    :return: A :class:list of :class:Qword objects.
    :rtype: list
    """
    # Convert the binary to a hexadecimal number as a string.
    hexstr = data.hex()

    # Slice the hex number into bytes. A byte in hexadecimal is two
    # digits long.
    pairs = []
    for i in range(0, len(hexstr), 2):
        pairs.append(hexstr[i:i + 2])

    # Store each group of eight bytes in a Qword dataclass object that
    # will become rows in a Table. A qword here is used to mean eight
    # bytes of data.
    results = []
    for i in range(0, len(pairs), 8):

        # This is the location of the qword within the file. The
        # trailing space is intentional. Tables don't allow you
        # to set passing around fields, so this is a hacky solution
        # for adding more visual separation to the Table when displayed.
        lineno = f'{i // 8 % 256:0>8b} '
        args = [lineno,]

        # Add the next eight bytes to the arguments.
        args += pairs[i:i + 8]

        # Build the Latin-1 translation of the bytes. Latin-1 here is
        # used because it is a one-byte character set. Every byte has a
        # character. No characters use more than one byte. Since most
        # English text is going to use characters in the bytes from 0x00
        # to 0x7F, it gives a quick idea of what is going on with any
        # English text in the file. While the characters for 0x80 to
        # 0xFF are less likely to match the intention of the data, they
        # may help the user discover useful patterns in the data.
        latin = data[i:i + 8].decode('latin_1')
        latin = remap_nonprintables(latin)
        latin = f' {latin}'

        # Add the data as a Qword into the list.
        qword = Qword(*args, in_latin=latin)
        results.append(qword)

    # Return the list of Qwords.
    return results


def handle_menu_selection(
    value: str,
    path: Path,
    q_to: Queue,
    show_hidden: bool = False
) -> None:
    """Update the terminal based on the option selected in the menu."""
    # Separate the file reading mode from the file to read. Since
    # panel action handlers have to return a single string, both
    # data are stored in the string, separated by a record separator
    # character.
    mode, selection = value.split('\x1e')

    # Remove the file or directory indicator added to the beginning
    # of the directory or file name.
    selection = selection[2:]

    # Update the path based on the selection.
    if selection == '..':
        path = path.parent
    else:
        path = path / Path(selection)

    # Determine whether the path is a directory or file and, if it's
    # a file, how the user wanted to view the file. Create the needed
    # panel based on that information.
    if path.is_dir():
        panel = create_dir_menu(path, show_hidden=show_hidden)
    elif mode == 'b':
        panel = create_binary_table(path)
    else:
        panel = create_text(path)

    # Create a unique key thurible.queue_manager can use to store and
    # show the panel. Then send the commands to queue_manager to store
    # and then show the panel.
    key = mode + '\x1e' + str(path)
    q_to.put(tm.Store(key, panel))
    q_to.put(tm.Show(key))

    # Return the updated path.
    return path


def parse_invocation() -> None:
    """Parse the command used to invoke filereader and pass any needed
    parameters to the mainline.
    """
    p = ArgumentParser(
        prog='filereader',
        description='A simple terminal file reader.'
    )
    p.add_argument(
        'path',
        help='The file or directory to open.',
        nargs='?',
        action='store',
        type=str,
        default=''
    )
    p.add_argument(
        '-H', '--show_hidden',
        help='Show hidden files and directories.',
        action='store_true'
    )
    args = p.parse_args()
    main(args.path, show_hidden=args.show_hidden)


def read_file_as_binary(path: str | Path) -> str:
    """Return the contents of the given file as bytes."""
    with open(path, 'rb') as fh:
        text = fh.read()
    return text


def read_file_as_text(path: str | Path, encoding: str = 'utf_8') -> str:
    """Return the contents of the given file as text."""
    with open(path, encoding=encoding) as fh:
        text = fh.read()
    return text


def remap_nonprintables(text: str) -> str:
    """Search the string for control characters and replace them with
    their unicode representation.
    """
    for i, char in enumerate(text):
        if ucd.category(char) == 'Cc':
            code = ord(char)
            new = chr(code + 0x2400)
            text = text[0:i] + new + text[i + 1:]
    return text


# Mainline.
def main(
    path: str = '',
    q_to: Optional[Queue] = None,
    q_from: Optional[Queue] = None,
    show_hidden: bool = False
) -> None:
    # If no path was given, default to the current working directory.
    path = Path(path) if path else Path().cwd()

    # Since thurible.queue_manager is designed to be used in a separate
    # thread or process, there needs to be shared queues to allow the
    # program to send commands to the manager and the manager to send
    # input and data back to the program.
    q_to = q_to if q_to else Queue()
    q_from = q_from if q_from else Queue()

    # The first panel displayed by filereader is a FileReaderMenu panel
    # containing the contents of the directory path that was given to
    # main().
    menu = create_dir_menu(path)

    # The program interacts with the manager by sending it Messages.
    msgs = [

        # The Store message tells the manager to store a panel with a
        # name that you can use in future messages to the manager. This
        # allows you to preload panels in the manager, showing them only
        # when you need.
        tm.Store(str(path), menu),

        # The Show message tells the manager to display the panel with the
        # given name in the terminal. This panel will then also be the
        # first to receive all input from the user.
        tm.Show(str(path))
    ]

    # Since the manager is running in a separate thread, you cannot
    # communicate to it directly. Messages need to be added to the
    # queue that sends messages to the manager.
    for msg in msgs:
        q_to.put(msg)

    # In thurible, a manager is used to send output to the terminal
    # and to receive input from the user. For filereader, we are using
    # the queued_manager, which is designed to be run in a separate
    # threat or process from the rest of your application. That way,
    # interaction with the terminal will not block the running of your
    # code and vice versa. This will create the thread for the manager
    # and start it.
    T = Thread(target=thb.queued_manager, args=(q_to, q_from))
    T.start()

    # Since the manager communicates through a queue, you need a loop
    # to check if there are messages in the queue and act on them.
    # There are probably many ways to do that. Here we are using a
    # simple while loop.
    alerting = ''
    while True:

        # If we've received a message, we may need to act.
        if not q_from.empty():

            # Get the message from the queue.
            msg = q_from.get()

            # Input from the user is passed to the currently displayed
            # panel first incase it's navigation input. If the panel
            # doesn't have a defined behavior for the input, the string
            # representation of that input is returned to you as a
            # Data message, so that your code can act on it.
            #
            # If an alert is showing, enter closes the alert.
            if (
                alerting
                and isinstance(msg, tm.Data)
                and msg.value == 'Continue'
            ):
                msg = tm.Dismiss(alerting)
                q_to.put(msg)
                alerting = ''

            # If an alert is showing, other keys do nothing.
            elif alerting and isinstance(msg, tm.Data):
                pass

            # If the user pressed the `q` key, quit the program.
            elif isinstance(msg, tm.Data) and msg.value == 'q':
                break

            # If the user pressed the escape key, send the directory
            # menu for the parent of the currently viewed directory
            # or file.
            elif isinstance(msg, tm.Data) and msg.value == '\x1b':
                path = path.parent
                panel = create_dir_menu(path, show_hidden=show_hidden)
                q_to.put(tm.Store(str(path), panel))
                q_to.put(tm.Show(str(path)))

            # If the user selected a menu item, the selection should
            # be handled.
            elif isinstance(msg, tm.Data) and '\x1e' in msg.value:
                path = handle_menu_selection(
                    msg.value,
                    path,
                    q_to,
                    show_hidden
                )

            # If the user supplied other input, show an alert.
            elif isinstance(msg, tm.Data):
                alerting = f'{msg.value} alert'
                msg = tm.Alert(
                    name=alerting,
                    title='Alert',
                    text=f'Unknown input: {msg.value}',
                    options=cont
                )
                q_to.put(msg)

            # If the queued_manager ends unexpectedly, it should send an
            # Ending message explaining why. The main cause of that
            # would be when an exception is raised. In that case, the
            # exception will be returned in the Ending message, so your
            # code can react to it.
            elif isinstance(msg, tm.Ending) and msg.ex:
                raise msg.ex

            # This is just here as a catch all in case there is some
            # reason other than an Exception that could cause the
            # manager to send an unexpected Ending message. That
            # should't happen with queued_manager, but may be possible
            # with managers developed in the future.
            elif isinstance(msg, tm.Ending):
                msg = f'queue_manager ended for reason: {msg.reason}'
                raise RuntimeError(msg)

    # Once filereader breaks out of the loop, it will end. Send an
    # End message to the manager to allow it to exit cleanly.
    q_to.put(tm.End())


if __name__ == '__main__':
    parse_invocation()
