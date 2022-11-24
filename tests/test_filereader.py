"""
test_filereader
~~~~~~~~~~~~~~~

Unit tests for the `filereader` example.
"""
from pathlib import Path
from queue import Queue
import unittest as ut
from unittest.mock import call, patch
import sys

from blessed import Terminal
from blessed.keyboard import Keystroke

from examples import filereader as fr
import thurible as thb
import thurible.messages as tm
from thurible import get_terminal, menu, Table, text


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


# Test cases.
class CreateDirMenuTestCase(ut.TestCase):
    def assertEqual(self, a, b):
        if (
            isinstance(a, menu.Menu)
            and isinstance(b, menu.Menu)
            and a != b
        ):
            for key in a.__dict__:
                super().assertEqual(getattr(a, key), getattr(b, key))
        super().assertEqual(a, b)

    def test_create_dir_menu(self):
        """Given a file path and the name of the parent directory,
        create_dir_menu() returns a menu to allow the user to select
        a path in that directory.
        """
        # Expected value.
        exp = fr.FileReaderMenu(
            options=CWD_OPTIONS,
            footer_text=DIR_FOOT,
            footer_frame=True,
            title_text='tests/data',
            title_frame=True,
            frame_type='double',
            height=term.height,
            width=term.width,
            term=term
        )

        # Test data and state.
        path = exp.title_text

        # Run test.
        act = fr.create_dir_menu(path)

        # Determine test success.
        self.assertEqual(exp.title_text, act.title_text)
        self.assertEqual(exp, act)

    @patch('examples.filereader.Path.cwd', return_value='tests/data')
    def test_create_dir_menu_with_no_path(self, _):
        """Given a file path and the name of the parent directory,
        `create_dir_menu()` returns a menu to allow the user to select
        a path in that directory. If no directory name is sent, the
        menu should show the contents of the current working directory.
        """
        # Expected value.
        exp = fr.FileReaderMenu(
            options=CWD_OPTIONS,
            footer_text=DIR_FOOT,
            footer_frame=True,
            title_text='tests/data',
            title_frame=True,
            frame_type='double',
            height=term.height,
            width=term.width,
            term=term
        )

        # Run test.
        act = fr.create_dir_menu()

        # Determine test success.
        self.assertEqual(exp, act)


class CreateTextTestCase(ut.TestCase):
    def assertEqual(self, a, b):
        try:
            super().assertEqual(a, b)
        except AssertionError as ex:
            if isinstance(a, text.Text) and isinstance(b, text.Text):
                self.assertEqual(a.content, b.content)
            raise ex

    def test_create_text(self):
        """Given the path to a text file, `create_text()` will return
        a text reader for the text contained in the file.
        """
        # Expected value.
        exp = text.Text(
            content='spam eggs bacon',
            title_text='tests/data/simple.txt',
            title_frame=True,
            footer_text=TEXT_FOOT,
            footer_frame=True,
            frame_type='heavy',
            height=term.height,
            width=term.width,
            term=term
        )

        # Test data and state.
        path = exp.title_text

        # Run test.
        act = fr.create_text(path)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_create_text_invalid_utf_8(self):
        """Given the path to a text file, `create_text()` will return
        a text reader for the text contained in the file. If the file
        contains invalid UTF-8 sequences, try opening as Latin-1
        instead.
        """
        # Expected value.
        exp = text.Text(
            content='\xc3\x28\n',
            title_text='tests/data/invalid_utf_8.txt',
            title_frame=True,
            footer_text=TEXT_FOOT,
            footer_frame=True,
            frame_type='heavy',
            height=term.height,
            width=term.width,
            term=term
        )

        # Test data and state.
        path = exp.title_text

        # Run test.
        act = fr.create_text(path)

        # Determine test result.
        self.assertEqual(exp, act)


class HandleMenuSelectionTestCase(ut.TestCase):
    def test_selecting_directory_creates_menu(self):
        """When passed a value and path that join to point to a
        directory, `handle_menu_selection()` should create a `menu.Menu`
        object with the contents of that directory, send that object and
        a message to show the object to the given queue.
        """
        # Expected values.
        exp = [
            tm.Store(
                '\n\x1etests/data/lyrics',
                fr.create_dir_menu('tests/data/lyrics')
            ),
            tm.Show('\n\x1etests/data/lyrics'),
        ]

        # Test data and state.
        value = '\n\x1e▸ lyrics'
        path = Path('tests/data')
        q_to = Queue()

        # Run test.
        fr.handle_menu_selection(value, path, q_to)

        # Get actual value.
        act = []
        while not q_to.empty():
            act.append(q_to.get())

        # Determine test result.
        self.assertEqual(exp, act)

    def test_selecting_file_creates_text(self):
        """When passed a value and path that join to point to a file,
        `handle_menu_selection()` should create a `text.Text` object
        with the contents of that file, send that object and a message
        to show the object to the given queue.
        """
        # Expected values.
        exp = [
            tm.Store(
                '\n\x1etests/data/simple.txt',
                fr.create_text('tests/data/simple.txt')
            ),
            tm.Show('\n\x1etests/data/simple.txt'),
        ]

        # Test data and state.
        value = '\n\x1e  simple.txt'
        path = Path('tests/data')
        q_to = Queue()

        # Run test.
        fr.handle_menu_selection(value, path, q_to)

        # Get actual value.
        act = []
        while not q_to.empty():
            act.append(q_to.get())

        # Determine test result.
        self.assertEqual(exp, act)

    def test_selecting_Parent_directory_creates_menu(self):
        """When passed a value and path that join to point to the parent
        directory, `handle_menu_selection()` should create a `menu.Menu`
        object with the contents of that directory, send that object and
        a message to show the object to the given queue.
        """
        # Expected values.
        exp = [
            tm.Store(
                '\n\x1etests',
                fr.create_dir_menu('tests')
            ),
            tm.Show('\n\x1etests'),
        ]

        # Test data and state.
        value = '\n\x1e▸ ..'
        path = Path('tests/data')
        q_to = Queue()

        # Run test.
        fr.handle_menu_selection(value, path, q_to)

        # Get actual value.
        act = []
        while not q_to.empty():
            act.append(q_to.get())

        # Determine test result.
        self.assertEqual(exp, act)


class InvocationTestCase(ut.TestCase):
    def setUp(self):
        self.original_argv = sys.argv

    def tearDown(self):
        sys.argv = self.original_argv

    @patch('examples.filereader.main')
    def invocation_test(self, exp, args, mock_main):
        # Test data and set up.
        args.insert(0, 'python -m examples.filereader')
        sys.argv = args

        # Run test.
        fr.parse_invocation()

        # Gather actual values.
        act = mock_main.mock_calls

        # Determine test result.
        self.assertEqual(exp, act)

    def test_no_arguments(self):
        """Given no invocation arguments, `parse_invocation()` should
        pass default parameters to `main()`.
        """
        exp = [call('', show_hidden=False),]
        args = []
        self.invocation_test(exp, args)

    def test_with_show_hidden(self):
        """Given `-H`, `parse_invocation()` should pass that file
        path to `main()`.
        """
        exp = [call('', show_hidden=True),]
        args = ['-H',]
        self.invocation_test(exp, args)

    def test_with_starting_path(self):
        """Given a file path, `parse_invocation()` should pass that file
        path to `main()`.
        """
        exp = [call('test/data', show_hidden=False),]
        args = ['test/data',]
        self.invocation_test(exp, args)


class MainTestCase(ut.TestCase):
    def setUp(self):
        self.q_to = Queue()
        self.q_from = Queue()
        self.term = get_terminal()

    @patch('examples.filereader.Path.cwd', return_value='tests/data')
    @patch('examples.filereader.Thread')
    def main_test(self, exp, data, kwargs, mock_thread, _):
        """When invoked, `main()` should run the manager for the UI
        on a new thread and send it messages with the initial menu
        panel and to display that panel.
        """
        # Expected values.
        exp_calls = [
            call(target=thb.queued_manager, args=(
                self.q_to,
                self.q_from,
                self.term
            )),
            call().start(),
        ]
        exp_msgs = [
            tm.Store('tests/data', fr.FileReaderMenu(
                options=CWD_OPTIONS,
                footer_text=DIR_FOOT,
                footer_frame=True,
                title_text='tests/data',
                title_frame=True,
                frame_type='double',
                height=self.term.height,
                width=self.term.width,
                term=self.term
            )),
            tm.Show('tests/data'),
            *exp,
            tm.End(''),
        ]

        # Test data and state.
        for msg in data:
            self.q_from.put(msg)

        # Run test.
        fr.main('', self.q_to, self.q_from, **kwargs)

        # Gather actual values.
        act_calls = mock_thread.mock_calls
        act_msgs = []
        while not self.q_to.empty():
            act_msgs.append(self.q_to.get())

        # Determine test result.
        self.assertEqual(exp_calls, act_calls)
        self.assertEqual(exp_msgs, act_msgs)

    def test_binary_escape_back_to_dir_menu(self):
        """Hitting escape when viewing a binary file sends the user back
        to the directory menu.
        """
        exp = [
            tm.Store(
                'b\x1etests/data/simple.txt',
                Table(
                    records=QWORDS,
                    footer_text=BIN_FOOT,
                    footer_frame=True,
                    title_text='tests/data/simple.txt',
                    title_frame=True,
                    frame_type='heavy',
                    height=term.height,
                    width=term.width,
                    term=term
                )
            ),
            tm.Show('b\x1etests/data/simple.txt'),
            tm.Store('tests/data', fr.FileReaderMenu(
                options=CWD_OPTIONS,
                footer_text=DIR_FOOT,
                footer_frame=True,
                title_text='tests/data',
                title_frame=True,
                frame_type='double',
                height=self.term.height,
                width=self.term.width,
                term=self.term
            )),
            tm.Show('tests/data'),
        ]
        data = [
            tm.Data('b\x1e  simple.txt'),
            tm.Data('\x1b'),
            tm.Data('q'),
        ]
        kwargs = {}
        self.main_test(exp, data, kwargs)

    def test_navigate_with_show_hidden(self):
        """If the `show_hidden` parameter is sent as true, `main()`
        should make the file menus show hidden files.
        """
        exp = [
            tm.Store('\n\x1etests/data/lyrics', fr.FileReaderMenu(
                options=[
                    menu.Option('▸ ..', ''),
                    menu.Option('  .secret.txt', ''),
                    menu.Option('  bohemian.txt', ''),
                ],
                footer_text=DIR_FOOT,
                footer_frame=True,
                title_text='tests/data/lyrics',
                title_frame=True,
                frame_type='double',
                height=self.term.height,
                width=self.term.width,
                term=self.term
            )),
            tm.Show('\n\x1etests/data/lyrics'),
        ]
        data = [tm.Data('\n\x1e▸ lyrics'), tm.Data('q'),]
        kwargs = {'show_hidden': True,}
        self.main_test(exp, data, kwargs)

    def test_open_binary(self):
        """When the user presses `b` when a file is selected in the
        file menu, the file should be opened in a binary view."""
        exp = [
            tm.Store(
                'b\x1etests/data/simple.txt',
                Table(
                    records=QWORDS,
                    footer_text=BIN_FOOT,
                    footer_frame=True,
                    title_text='tests/data/simple.txt',
                    title_frame=True,
                    frame_type='heavy',
                    height=term.height,
                    width=term.width,
                    term=term
                )
            ),
            tm.Show('b\x1etests/data/simple.txt'),
        ]
        data = [
            tm.Data('b\x1e  simple.txt'),
            tm.Data('q'),
        ]
        kwargs = {}
        self.main_test(exp, data, kwargs)

    def test_open_text(self):
        """When the user presses enter when a file is selected in the
        file menu, the file should be opened in a text view.
        """
        exp = [
            tm.Store(
                '\n\x1etests/data/simple.txt',
                text.Text(
                    content='spam eggs bacon',
                    title_text='tests/data/simple.txt',
                    title_frame=True,
                    footer_text=TEXT_FOOT,
                    footer_frame=True,
                    frame_type='heavy',
                    height=term.height,
                    width=term.width,
                    term=term
                )
            ),
            tm.Show('\n\x1etests/data/simple.txt'),
        ]
        data = [
            tm.Data('\n\x1e  simple.txt'),
            tm.Data('q'),
        ]
        kwargs = {}
        self.main_test(exp, data, kwargs)

    def test_quit(self):
        """`main()` should end if the user types `q`."""
        exp = []
        data = [tm.Data('q'),]
        kwargs = {}
        self.main_test(exp, data, kwargs)

    def test_text_escape_back_to_dir_menu(self):
        """Hitting escape when viewing a text file sends the user back
        to the directory menu.
        """
        exp = [
            tm.Store('\n\x1etests/data/simple.txt', text.Text(
                content='spam eggs bacon',
                title_text='tests/data/simple.txt',
                title_frame=True,
                footer_text=TEXT_FOOT,
                footer_frame=True,
                frame_type='heavy',
                height=term.height,
                width=term.width,
                term=term
            )),
            tm.Show('\n\x1etests/data/simple.txt'),
            tm.Store('tests/data', fr.FileReaderMenu(
                options=CWD_OPTIONS,
                footer_text=DIR_FOOT,
                footer_frame=True,
                title_text='tests/data',
                title_frame=True,
                frame_type='double',
                height=self.term.height,
                width=self.term.width,
                term=self.term
            )),
            tm.Show('tests/data'),
        ]
        data = [
            tm.Data('\n\x1e  simple.txt'),
            tm.Data('\x1b'),
            tm.Data('q'),
        ]
        kwargs = {}
        self.main_test(exp, data, kwargs)


class PublicFunctionTestCase(ut.TestCase):
    def test_create_binary_table(self):
        """Given the path to a file, `create_binary_table()` will
        return a table for displaying the data in the file as
        hexadecimal.
        """
        # Expected value.
        exp = Table(
            records=QWORDS,
            footer_text=BIN_FOOT,
            footer_frame=True,
            title_text='tests/data/simple.txt',
            title_frame=True,
            frame_type='heavy',
            height=term.height,
            width=term.width,
            term=term
        )

        # Test data and state.
        path = exp.title_text

        # Run test.
        act = fr.create_binary_table(path)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_create_options_from_paths(self):
        """When called with a list of file paths, create_options_from_paths()
        returns a list of options where the names of each options are the
        names of the files and directories in those paths. Those names
        should be prefixed with a character indicating whether they are
        files or directories.
        """
        # Expected value.
        exp = [
            menu.Option('▸ ..', ''),
            menu.Option('▸ lyrics', ''),
            menu.Option('  simple.txt', ''),
            menu.Option('  spam.txt', ''),
        ]

        # Test data and state.
        paths = [
            Path('tests/data/lyrics'),
            Path('tests/data/spam.txt'),
            Path('tests/data/simple.txt'),
        ]

        # Run test.
        act = fr.create_options_from_paths(paths)

        # Determine test success.
        self.assertEqual(exp, act)

    def test_create_options_from_paths_hide_hidden(self):
        """When called with a list of file paths, create_options_from_paths()
        returns a list of options where the names of each options are the
        names of the files and directories in those paths. Those names
        should be prefixed with a character indicating whether they are
        files or directories. If any of the file or directory names start
        with a period, they will will not be returned as an option.
        """
        # Expected value.
        exp = [
            menu.Option('▸ ..', ''),
            menu.Option('▸ lyrics', ''),
            menu.Option('  simple.txt', ''),
            menu.Option('  spam.txt', ''),
        ]

        # Test data and state.
        paths = [
            Path('tests/data/lyrics'),
            Path('tests/data/spam.txt'),
            Path('tests/data/.hidden.txt'),
            Path('tests/data/simple.txt'),
        ]

        # Run test.
        act = fr.create_options_from_paths(paths)

        # Determine test success.
        self.assertEqual(exp, act)

    def test_create_options_from_paths_show_hidden(self):
        """When called with a list of file paths and a flag saying hidden
        files should be shown, create_options_from_paths() returns a list
        of options where the names of each options are the names of the
        files and directories in those paths. Those names should be
        prefixed with a character indicating whether they are files or
        directories.
        """
        # Expected value.
        exp = [
            menu.Option('▸ ..', ''),
            menu.Option('▸ lyrics', ''),
            menu.Option('  .hidden.txt', ''),
            menu.Option('  simple.txt', ''),
            menu.Option('  spam.txt', ''),
        ]

        # Test data and state.
        paths = [
            Path('tests/data/lyrics'),
            Path('tests/data/spam.txt'),
            Path('tests/data/.hidden.txt'),
            Path('tests/data/simple.txt'),
        ]
        show_hidden = True

        # Run test.
        act = fr.create_options_from_paths(paths, show_hidden)

        # Determine test success.
        self.assertEqual(exp, act)

    def test_get_dir_list(self):
        """When called with a file path that is a directory,
        get_dir_list() returns the contents of the directory.
        """
        # Expected value.
        exp = CWD_PATHS

        # Test data and state.
        path = 'tests/data'

        # Run test.
        act = fr.get_dir_list(path)

        # Determine test result.
        self.assertListEqual(exp, act)

    def test_get_hex(self):
        """Given a bytes, return a list that contains the hexadecimal
        number for each byte of data in the bytes as a two character
        string.
        """
        # Expected value.
        exp = QWORDS

        # Test data and state.
        b = b'spam eggs bacon'

        # Run test.
        act = fr.get_hex(b)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_read_file_as_binary(self):
        """When called with a file path that is a file,
        read_file_as_text() opens the file and returns the
        contents of the file as bytes.
        """
        # Expected value.
        exp = b'spam eggs bacon'

        # Test data and state.
        path = Path('tests/data/simple.txt')

        # Run test.
        act = fr.read_file_as_binary(path)

        # Determine test success.
        self.assertEqual(exp, act)

    def test_read_file_as_text(self):
        """When called with a file path that is a file,
        read_file_as_text() opens the file and returns the
        contents of the file as a text string.
        """
        # Expected value.
        exp = 'spam eggs bacon'

        # Test data and state.
        path = Path('tests/data/simple.txt')

        # Run test.
        act = fr.read_file_as_text(path)

        # Determine test success.
        self.assertEqual(exp, act)

    def test_remap_nonprintables(self):
        """Given a string, `remap_nonprintables()` converts the
        non-printable ASCII characters in that string to their
        representative unicode character.
        """
        # Expected value.
        exp = 'spam␊␍'

        # Test data and state.
        text = 'spam\n\r'

        # Run test.
        act = fr.remap_nonprintables(text)

        # Determine test results.
        self.assertEqual(exp, act)
