"""
test_filereader
~~~~~~~~~~~~~~~

Unit tests for the `filereader` example.
"""
from pathlib import Path
from queue import Queue

import pytest as pt
from blessed import Terminal
from blessed.keyboard import Keystroke

import thurible as thb
import thurible.messages as tm
from examples import filereader as fr
from thurible import Table, get_terminal, menu, text


# Common values.
term = Terminal()
BIN_FOOT = '\u241b:Back q:Quit'
DIR_FOOT = '⏎:Text b:Bin q:Quit'
TEXT_FOOT = '\u241b:Back q:Quit'
CWD_PATHS = [
    Path('tests/data/lyrics'),
    Path('tests/data/invalid_utf_8.txt'),
    Path('tests/data/spam.txt'),
    Path('tests/data/simple.txt'),
]
CWD_OPTIONS = [
    menu.Option('▸ ..', ''),
    menu.Option('▸ lyrics', ''),
    menu.Option('  invalid_utf_8.txt', ''),
    menu.Option('  simple.txt', ''),
    menu.Option('  spam.txt', ''),
]
QWORDS = [
    fr.Qword(
        '00000000 ',
        '73', '70', '61', '6d',
        '20', '65', '67', '67',
        ' spam egg'
    ),
    fr.Qword(
        '00000001 ',
        '73', '20', '62', '61',
        '63', '6f', '6e', '',
        ' s bacon'
    ),
]


# Fixtures.
@pt.fixture
def in_test_data(mocker):
    path = Path('tests/data')
    mocker.patch('pathlib.Path.cwd', return_value=path)
    yield path


@pt.fixture
def mock_thread(mocker):
    mocked = mocker.patch('examples.filereader.Thread')
    yield mocked


# Test cases.
class TestCreateDirMenu:
    def test_with_path(self, capsys, term):
        """Given a file path and the name of the parent directory,
        create_dir_menu() returns a menu to allow the user to select
        a path in that directory.
        """
        path = 'tests/data'
        menu = fr.create_dir_menu(path)
        assert menu.options == CWD_OPTIONS
        assert menu.footer_text == DIR_FOOT
        assert menu.footer_frame
        assert menu.title_text == path
        assert menu.frame_type == 'double'
        assert menu.height == term.height
        assert menu.width == term.width
        assert menu.term == term

    def test_no_path(self, capsys, in_test_data, term):
        """Given a file path and the name of the parent directory,
        `create_dir_menu()` returns a menu to allow the user to select
        a path in that directory. If no directory name is sent, the
        menu should show the contents of the current working directory.
        """
        path = str(in_test_data)
        menu = fr.create_dir_menu()
        assert menu.options == CWD_OPTIONS
        assert menu.footer_text == DIR_FOOT
        assert menu.footer_frame
        assert menu.title_text == path
        assert menu.frame_type == 'double'
        assert menu.height == term.height
        assert menu.width == term.width
        assert menu.term == term


class TestCreateText:
    def test_valid_utf8(self, capsys, term):
        """Given the path to a text file, `create_text()` will return
        a text reader for the text contained in the file.
        """
        path = 'tests/data/simple.txt'
        text = fr.create_text(path)
        assert text.content == 'spam eggs bacon'
        assert text.title_text == path
        assert text.title_frame
        assert text.footer_text == TEXT_FOOT
        assert text.footer_frame
        assert text.frame_type == 'heavy'
        assert text.height == term.height
        assert text.width == term.width
        assert text.term == term

    def test_invalid_utf8(self, capsys, term):
        """Given the path to a text file, `create_text()` will return
        a text reader for the text contained in the file. If the file
        contains invalid UTF-8 sequences, try opening as Latin-1
        instead.
        """
        path = 'tests/data/invalid_utf_8.txt'
        text = fr.create_text(path)
        assert text.content == '\xc3\x28\n'
        assert text.title_text == path


class TestHandleMenuSelection:
    def test_selecting_directory_creates_menu(self, capsys):
        """When passed a value and path that join to point to a
        directory, `handle_menu_selection()` should create a `menu.Menu`
        object with the contents of that directory, send that object and
        a message to show the object to the given queue.
        """
        value = '\n\x1e▸ lyrics'
        path = Path('tests/data')
        q_to = Queue()

        fr.handle_menu_selection(value, path, q_to)
        assert q_to.get() == tm.Store(
            '\n\x1etests/data/lyrics',
            fr.create_dir_menu('tests/data/lyrics')
        )
        assert q_to.get() == tm.Show('\n\x1etests/data/lyrics')
        assert q_to.empty()

    def test_selecting_file_creates_text(self, capsys):
        """When passed a value and path that join to point to a file,
        `handle_menu_selection()` should create a `text.Text` object
        with the contents of that file, send that object and a message
        to show the object to the given queue.
        """
        value = '\n\x1e  simple.txt'
        path = Path('tests/data')
        q_to = Queue()

        fr.handle_menu_selection(value, path, q_to)
        assert q_to.get() == tm.Store(
            '\n\x1etests/data/simple.txt',
            fr.create_text('tests/data/simple.txt')
        )
        assert q_to.get() == tm.Show('\n\x1etests/data/simple.txt')
        assert q_to.empty()

    def test_selecting_parent_creates_menu(self, capsys):
        """When passed a value and path that join to point to the parent
        directory, `handle_menu_selection()` should create a `menu.Menu`
        object with the contents of that directory, send that object and
        a message to show the object to the given queue.
        """
        value = '\n\x1e▸ ..'
        path = Path('tests/data')
        q_to = Queue()

        fr.handle_menu_selection(value, path, q_to)
        assert q_to.get() == tm.Store(
            '\n\x1etests',
            fr.create_dir_menu('tests')
        )
        assert q_to.get() == tm.Show('\n\x1etests')
        assert q_to.empty()


class TestMain:
    def invocation_test(self, data, kwargs, queues, term):
        """When invoked, `main()` should run the manager for the UI
        on a new thread and send it messages with the initial menu
        panel and to display that panel.
        """
        q_to, q_from = queues
        for msg in data:
            q_from.put(msg)

        fr.main('', q_to, q_from, **kwargs)
        assert q_to.get() == tm.Store('tests/data', fr.FileReaderMenu(
            options=CWD_OPTIONS,
            footer_text=DIR_FOOT,
            footer_frame=True,
            title_text='tests/data',
            title_frame=True,
            frame_type='double',
            height=term.height,
            width=term.width,
            term=term
        ))
        assert q_to.get() == tm.Show('tests/data')
        return q_to

    def test_binary_escape_back_to_dir_menu(
        self, capsys, in_test_data, mock_thread, queues, term
    ):
        """Hitting escape when viewing a binary file sends the user back
        to the directory menu.
        """
        data = [
            tm.Data('b\x1e  simple.txt'),
            tm.Data('\x1b'),
            tm.Data('q'),
        ]
        kwargs = {}

        q_to = self.invocation_test(data, kwargs, queues, term)
        assert q_to.get() == tm.Store(
            'b\x1etests/data/simple.txt',
            Table(
                records=QWORDS,
                footer_text=BIN_FOOT,
                footer_frame=True,
                title_text='tests/data/simple.txt',
                title_frame=True,
                frame_type='heavy'
            )
        )
        assert q_to.get() == tm.Show('b\x1etests/data/simple.txt')
        assert q_to.get() == tm.Store('tests/data', fr.FileReaderMenu(
            options=CWD_OPTIONS,
            footer_text=DIR_FOOT,
            footer_frame=True,
            title_text='tests/data',
            title_frame=True,
            frame_type='double'
        ))
        assert q_to.get() == tm.Show('tests/data')
        assert q_to.get() == tm.End()
        assert q_to.empty()

    def test_navigate_with_show_hidden(
        self, capsys, in_test_data, mock_thread, queues, term
    ):
        """If the `show_hidden` parameter is sent as true, `main()`
        should make the file menus show hidden files.
        """
        data = [tm.Data('\n\x1e▸ lyrics'), tm.Data('q'),]
        kwargs = {'show_hidden': True,}

        q_to = self.invocation_test(data, kwargs, queues, term)
        assert q_to.get() == tm.Store(
            '\n\x1etests/data/lyrics',
            fr.FileReaderMenu(
                options=[
                    menu.Option('▸ ..', ''),
                    menu.Option('  .secret.txt', ''),
                    menu.Option('  bohemian.txt', ''),
                ],
                footer_text=DIR_FOOT,
                footer_frame=True,
                title_text='tests/data/lyrics',
                title_frame=True,
                frame_type='double'
            )
        )
        assert q_to.get() == tm.Show('\n\x1etests/data/lyrics')
        assert q_to.get() == tm.End()
        assert q_to.empty()

    def test_open_binary(
        self, capsys, in_test_data, mock_thread, queues, term
    ):
        """When the user presses `b` when a file is selected in the
        file menu, the file should be opened in a binary view.
        """
        data = [
            tm.Data('b\x1e  simple.txt'),
            tm.Data('q'),
        ]
        kwargs = {}

        q_to = self.invocation_test(data, kwargs, queues, term)
        assert q_to.get() == tm.Store(
            'b\x1etests/data/simple.txt',
            Table(
                records=QWORDS,
                footer_text=BIN_FOOT,
                footer_frame=True,
                title_text='tests/data/simple.txt',
                title_frame=True,
                frame_type='heavy'
            )
        )
        assert q_to.get() == tm.Show('b\x1etests/data/simple.txt')
        assert q_to.get() == tm.End()
        assert q_to.empty()

    def test_open_text(
        self, capsys, in_test_data, mock_thread, queues, term
    ):
        """When the user presses enter when a file is selected in the
        file menu, the file should be opened in a text view.
        """
        data = [
            tm.Data('\n\x1e  simple.txt'),
            tm.Data('q'),
        ]
        kwargs = {}

        q_to = self.invocation_test(data, kwargs, queues, term)
        assert q_to.get() == tm.Store(
            '\n\x1etests/data/simple.txt',
            text.Text(
                content='spam eggs bacon',
                title_text='tests/data/simple.txt',
                title_frame=True,
                footer_text=TEXT_FOOT,
                footer_frame=True,
                frame_type='heavy'
            )
        )
        assert q_to.get() == tm.Show('\n\x1etests/data/simple.txt')
        assert q_to.get() == tm.End()
        assert q_to.empty()

    def test_quit(
        self, capsys, in_test_data, mock_thread, queues, term
    ):
        """`main()` should end if the user types `q`."""
        data = [
            tm.Data('\n\x1e  simple.txt'),
            tm.Data('\x1b'),
            tm.Data('q'),
        ]
        kwargs = {}

        q_to = self.invocation_test(data, kwargs, queues, term)
        assert q_to.get() == tm.Store(
            '\n\x1etests/data/simple.txt',
            text.Text(
                content='spam eggs bacon',
                title_text='tests/data/simple.txt',
                title_frame=True,
                footer_text=TEXT_FOOT,
                footer_frame=True,
                frame_type='heavy'
            )
        )
        assert q_to.get() == tm.Show('\n\x1etests/data/simple.txt')
        assert q_to.get() == tm.Store(
            'tests/data',
            fr.FileReaderMenu(
                options=CWD_OPTIONS,
                footer_text=DIR_FOOT,
                footer_frame=True,
                title_text='tests/data',
                title_frame=True,
                frame_type='double'
            )
        )
        assert q_to.get() == tm.Show('tests/data')
        assert q_to.get() == tm.End()
        assert q_to.empty()


def test_create_binary_table(term):
    """Given the path to a file, `create_binary_table()` will
    return a table for displaying the data in the file as
    hexadecimal.
    """
    path = 'tests/data/simple.txt'
    table = fr.create_binary_table(path)
    assert table.records == QWORDS
    assert table.footer_text == BIN_FOOT
    assert table.footer_frame
    assert table.title_text == path
    assert table.title_frame
    assert table.frame_type == 'heavy'
    assert table.height == term.height
    assert table.width == term.width
    assert table.term == term


class TestCreateOptionsFromPaths:
    def test_create_options_from_paths(self, test_data_contents):
        """When called with a list of file paths, create_options_from_paths()
        returns a list of options where the names of each options are the
        names of the files and directories in those paths. Those names
        should be prefixed with a character indicating whether they are
        files or directories.
        """
        options = fr.create_options_from_paths(
            test_data_contents,
            show_hidden=True
        )
        assert options == [
            menu.Option('▸ ..', ''),
            menu.Option('▸ lyrics', ''),
            menu.Option('  .hidden.txt', ''),
            menu.Option('  invalid_utf_8.txt', ''),
            menu.Option('  simple.txt', ''),
            menu.Option('  spam.txt', ''),
        ]

    def test_create_options_from_paths_hide_hidden(self, test_data_contents):
        """When called with a list of file paths, create_options_from_paths()
        returns a list of options where the names of each options are the
        names of the files and directories in those paths. Those names
        should be prefixed with a character indicating whether they are
        files or directories. If any of the file or directory names start
        with a period, they will will not be returned as an option.
        """
        options = fr.create_options_from_paths(test_data_contents)
        assert options == [
            menu.Option('▸ ..', ''),
            menu.Option('▸ lyrics', ''),
            menu.Option('  invalid_utf_8.txt', ''),
            menu.Option('  simple.txt', ''),
            menu.Option('  spam.txt', ''),
        ]


def test_get_dir_list(test_data_contents):
    """When called with a file path that is a directory,
    get_dir_list() returns the contents of the directory.
    """
    path = 'tests/data'
    result = fr.get_dir_list(path)
    assert result == test_data_contents


def test_get_hex():
    """Given a bytes, return a list that contains the hexadecimal
    number for each byte of data in the bytes as a two character
    string.
    """
    b = b'spam eggs bacon'
    assert fr.get_hex(b) == QWORDS


def test_read_file_as_binary():
    """When called with a file path that is a file,
    read_file_as_text() opens the file and returns the
    contents of the file as bytes.
    """
    path = Path('tests/data/simple.txt')
    assert fr.read_file_as_binary(path) == b'spam eggs bacon'


def test_read_file_as_text():
    """When called with a file path that is a file,
    read_file_as_text() opens the file and returns the
    contents of the file as a text string.
    """
    path = Path('tests/data/simple.txt')
    assert fr.read_file_as_text(path) == 'spam eggs bacon'


def test_remap_nonprintables():
    """Given a string, `remap_nonprintables()` converts the
    non-printable ASCII characters in that string to their
    representative unicode character.
    """
    assert fr.remap_nonprintables('spam\n\r') == 'spam␊␍'
