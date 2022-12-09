"""
test_thurible
~~~~~~~~~~~~~~~~

Unit tests for the `thurible.thurible` module.
"""
from collections.abc import Iterator
from queue import Queue
import unittest as ut
from unittest.mock import call, patch, PropertyMock
from threading import Thread
from time import sleep

from blessed import Terminal
from blessed.keyboard import Keystroke

from thurible import log
from thurible import messages as tm
from thurible import thurible as thb
from thurible import dialog, menu, splash
from tests import test_panel as tp


# Common data.
term = Terminal()
KEY_DOWN = Keystroke('\x1b[B', term.KEY_DOWN, 'KEY_DOWN')
KEY_E = Keystroke('e')
KEY_END = Keystroke('\x1b[F', term.KEY_END, 'KEY_END')
KEY_ENTER = Keystroke('\n', term.KEY_ENTER, 'KEY_ENTER')
KEY_HOME = Keystroke('\x1b[H', term.KEY_HOME, 'KEY_HOME')
KEY_O = Keystroke('o')
KEY_PGDOWN = Keystroke('\x1b[U', term.KEY_PGDOWN, 'KEY_PGDOWN')
KEY_PGUP = Keystroke('\x1b[V', term.KEY_PGUP, 'KEY_PGUP')
KEY_UP = Keystroke('\x1b[A', term.KEY_UP, 'KEY_UP')
KEY_X = Keystroke('x')


# Utility classes and functions.
class EndlessSideEffect(Iterator):
    def __init__(self, values, on=True, *args, **kwargs):
        self.values = values
        self.index = 0
        self.on = on
        super().__init__(*args, **kwargs)

    def __next__(self):
        if not self.on:
            return None
        if self.index == len(self.values):
            return None
        value = self.values[self.index]
        self.index += 1
        return value


def empty_response():
    return None


# Test cases.
class QueuedManagerTestCase(tp.TerminalTestCase):
    def setUp(self):
        self.q_to = Queue()
        self.q_from = Queue()
        self.displays = {}
        self.t = Thread(target=thb.queued_manager, kwargs={
            'q_to': self.q_to,
            'q_from': self.q_from,
            'displays': self.displays,
        })

    def tearDown(self):
        if self.t.is_alive():
            self.q_to.put(tm.End())

    # Utility methods.
    def _watch_for_pong(self, name='', msg=None):
        """Send a ping to the queued_manager and wait for the pong
        response, collecting all responses received before the pong.
        This is usually done to ensure the queue_manager thread has
        had time to process all of the previous messages sent to it.
        """
        if not msg:
            ping = tm.Ping(name)
            msg = tm.Pong(name)
            self.q_to.put(ping)
        count = 0
        resp = None
        resps = []
        while resp != msg:
            if resp:
                resps.append(resp)
                if isinstance(resp, tm.Ending):
                    break
                resp = None
            if not self.q_from.empty():
                resp = self.q_from.get()
            if count > 100:
                raise RuntimeError('Ran too long.')
            count += 1
            sleep(.01)
        return resps

    # Patching handlers for simple tests.
    @patch('blessed.Terminal.fullscreen')
    @patch('blessed.Terminal.inkey')
    @patch('blessed.Terminal.cbreak')
    @patch('thurible.thurible.print')
    def _get_delayed_input(
        self,
        msgs,
        inputs,
        mock_print,
        mock_cbreak,
        mock_inkey,
        mock_fullscreen
    ):
        mock_inkey.side_effect = inputs
        for msg in msgs:
            if isinstance(msg, tm.Ping):
                ping_name = msg.name
        self.t.start()
        for msg in msgs:
            self.q_to.put(msg)
        act = None
        count = 0
        while not act:
            if not self.q_from.empty():
                msg = self.q_from.get()
                if isinstance(msg, tm.Pong) and msg.name == ping_name:
                    inputs.on = True
                else:
                    act = msg
            if count > 100:
                raise RuntimeError('No response after 100 tries.')
            count += 1
            sleep(.01)
        return act

    @patch('blessed.Terminal.fullscreen')
    @patch('blessed.Terminal.inkey')
    @patch('blessed.Terminal.cbreak')
    @patch('thurible.thurible.print')
    def _get_input(
        self,
        msgs,
        inputs,
        mock_print,
        mock_cbreak,
        mock_inkey,
        mock_fullscreen
    ):
        mock_inkey.side_effect = inputs
        self.t.start()
        for msg in msgs:
            self.q_to.put(msg)
        act = None
        count = 0
        while not act:
            if not self.q_from.empty():
                act = self.q_from.get()
            if count > 100:
                raise RuntimeError('No response after 100 tries.')
            count += 1
            sleep(.01)
        return act

    @patch('blessed.Terminal.fullscreen')
    @patch('thurible.thurible.print')
    def _get_msg_response(
        self,
        msgs,
        name,
        mock_print,
        mock_fullscreen
    ):
        self.t.start()
        for msg in msgs:
            self.q_to.put(msg)
        resps = self._watch_for_pong(name)
        return resps

    @patch('blessed.Terminal.fullscreen')
    @patch('thurible.thurible.print')
    def _send_msgs(
        self,
        msgs,
        name,
        will_end,
        mock_print,
        mock_fullscreen
    ):
        self.t.start()
        for msg in msgs:
            self.q_to.put(msg)
        if not will_end:
            _ = self._watch_for_pong(name)
        else:
            end = tm.Ending('Received End message.')
            _ = self._watch_for_pong(msg=end)
        return mock_print.mock_calls

    # Simple tests.
    def test_delete_display(self):
        """Sent a Delete message, queued_manager() should delete the
        Panel with the given name from the stored panels.
        """
        # Expected value.
        exp = {'spam': splash.Splash('spam'),}

        # Test data and state.
        eggs = splash.Splash('eggs')
        msgs = [
            tm.Store('eggs', eggs),
            tm.Store('spam', exp['spam']),
            tm.Delete('eggs'),
        ]

        # Run test and gather actual.
        self._send_msgs(msgs, 'test_store_display', False)
        act = self.displays

        # Determine test result.
        self.assertDictEqual(exp, act)

    def test_display_alert(self):
        """Sent an Alert message, queued_manager() should display an
        alert panel over the top of the current panel. Sent a Dismiss
        message, queued_manager() should restore the current panel.
        """
        # Expected values.
        exp = [
            call((
                f'{term.move(0, 0)}                              '
                f'{term.move(1, 0)}                              '
                f'{term.move(2, 0)}                              '
                f'{term.move(3, 0)}                              '
                f'{term.move(4, 0)}                              '
                f'{term.move(5, 0)}                              '
                f'{term.move(6, 0)}                              '
                f'{term.move(7, 0)}                              '
                f'{term.move(8, 0)}                              '
                f'{term.move(9, 0)}                              '
                f'{term.move(4, 13)}spam'
            ), end='', flush=True),
            call((
                f'{term.move(3, 7)}                '
                f'{term.move(4, 7)}                '
                f'{term.move(5, 7)}                '
                f'{term.move(6, 7)}                '
                f'{term.move(2, 6)}┌────────────────┐'
                f'{term.move(3, 6)}│'
                f'{term.move(3, 23)}│'
                f'{term.move(4, 6)}│'
                f'{term.move(4, 23)}│'
                f'{term.move(5, 6)}│'
                f'{term.move(5, 23)}│'
                f'{term.move(6, 6)}│'
                f'{term.move(6, 23)}│'
                f'{term.move(7, 6)}└────────────────┘'
                f'{term.move(4, 7)}?spam spam spam'
                f'{term.move(5, 7)}spam?'
                f'{term.reverse}'
                f'{term.move(6, 19)}[No]'
                f'{term.normal}'
                f'{term.move(6, 13)}[Yes]'
            ), end='', flush=True),
            call((
                f'{term.move(0, 0)}                              '
                f'{term.move(1, 0)}                              '
                f'{term.move(2, 0)}                              '
                f'{term.move(3, 0)}                              '
                f'{term.move(4, 0)}                              '
                f'{term.move(5, 0)}                              '
                f'{term.move(6, 0)}                              '
                f'{term.move(7, 0)}                              '
                f'{term.move(8, 0)}                              '
                f'{term.move(9, 0)}                              '
                f'{term.move(4, 13)}spam'
            ), end='', flush=True),
        ]

        # Test data and state.
        s = splash.Splash(
            content='spam',
            height=10,
            width=30,
            term=Terminal()
        )
        msgs = [
            tm.Store('spam', s),
            tm.Show('spam'),
            tm.Alert(
                'test_display_alert',
                '',
                '?spam spam spam spam?',
                dialog.yes_no
            ),
            tm.Dismiss('test_display_alert'),
        ]

        # Run test.
        act = self._send_msgs(msgs, 'test_show_display', False)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_get_display(self):
        """Sent a `Showing` message, queued_manager() should return a
        `Shown` message with the currently displayed panel.
        """
        # Expected value.
        exp = [tm.Shown('test_get_display', 'spam'),]

        # Test data and state.
        s = splash.Splash('eggs')
        msgs = [
            tm.Store(exp[0].display, s),
            tm.Show(exp[0].display),
            tm.Showing(exp[0].name),
        ]

        # Run test.
        act = self._get_msg_response(msgs, 'test_show_display')

        # Determine test result.
        self.assertListEqual(exp, act)

    def test_list_stored_display(self):
        """Sent a `Storing` message, queued_manager() should return a
        `Stored` message with a list of stored panels.
        """
        # Expected value.
        exp = [tm.Stored('ham', ('spam', 'eggs', 'bacon',)),]

        # Test data and state.
        msgs = [
            tm.Store(exp[0].stored[0], splash.Splash(exp[0].stored[0])),
            tm.Store(exp[0].stored[1], splash.Splash(exp[0].stored[1])),
            tm.Store(exp[0].stored[2], splash.Splash(exp[0].stored[2])),
            tm.Storing(exp[0].name),
        ]

        # Run test.
        act = self._get_msg_response(msgs, 'test_list_stored_display')

        # Determine test result.
        self.assertListEqual(exp, act)

    def test_print_farewell(self):
        """Sent an End message with a farewell string, the farewell
        string should be printed as the queued_manager() terminates.
        """
        # Expected value.
        exp = [call('spam'),]

        # Test data and state.
        msgs = [tm.End('spam'),]

        # Run test.
        act = self._send_msgs(msgs, 'test_print_farewell', True)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_sends_selection_from_menu(self):
        """Receiving input from the user that isn't acted on by the
        display, `queued_manager()` should send the input to the
        application as a Data message.
        """
        # Expected value.
        exp = tm.Data('eggs')

        # Test data and state.
        inputs = EndlessSideEffect([
            KEY_DOWN,
            KEY_ENTER
        ], False)
        msgs = [
            tm.Store('menu', menu.Menu(
                [
                    menu.Option('spam', 's'),
                    menu.Option('eggs', 'e'),
                    menu.Option('bacon', 'b'),
                ],
                height=5,
                width=7,
                term=term
            )),
            tm.Show('menu'),
            tm.Ping('test_sends_selection_from_menu'),
        ]

        # Run test and gather actual.
        act = self._get_delayed_input(msgs, inputs)

        # Determine test results.
        self.assertEqual(exp, act)

    def test_sends_exception(self):
        """When an exception is raised in queued_manager, it sends the
        exception to the program and ends.
        """
        # Expected value.
        exp = [tm.Ending('Exception.', ValueError('eggs')),]

        # Test data and state.
        class Spam(splash.Splash):
            def __str__(self):
                raise exp[0].ex

        s = Spam(
            content='spam',
            height=5,
            width=6,
            term=Terminal()
        )
        msgs = [
            tm.Store('spam', s),
            tm.Show('spam'),
        ]

        # Run test.
        act = self._get_msg_response(msgs, 'test_show_display')

        # Determine test result.
        self.assertListEqual(exp, act)

    def test_sends_input_to_application(self):
        """Receiving input from the user that isn't acted on by the'
        display, `queued_manager()` should send the input to the
        application as a Data message.
        """
        # Expected value.
        exp = tm.Data('x')

        # Test data and state.
        inputs = EndlessSideEffect([KEY_X,])
        s = splash.Splash(
            content='spam',
            height=5,
            width=6,
            term=Terminal()
        )
        msgs = [
            tm.Store('spam', s),
            tm.Show('spam'),
        ]

        # Run test and gather actual.
        act = self._get_input(msgs, inputs)

        # Determine test results.
        self.assertEqual(exp, act)

    def test_show_display(self):
        """Sent a Show message, queued_manager() should write the
        string to the terminal.
        """
        # Expected value.
        exp = [call((
            f'{term.move(0, 0)}                    '
            f'{term.move(1, 0)}                    '
            f'{term.move(2, 0)}                    '
            f'{term.move(3, 0)}                    '
            f'{term.move(4, 0)}                    '
            f'{term.move(2, 8)}spam'
        ), end='', flush=True),]

        # Test data and state.
        s = splash.Splash(
            content='spam',
            height=5,
            width=20,
            term=Terminal()
        )
        msgs = [
            tm.Store('spam', s),
            tm.Show('spam'),
        ]

        # Run test.
        act = self._send_msgs(msgs, 'test_show_display', False)

        # Determine test result.
        self.assertListEqual(exp, act)

    def test_store_display(self):
        """Sent a Store message, queued_manager() should store the
        contained Display for later use.
        """
        # Expected value.
        exp = {'spam': splash.Splash(
            content='spam',
            height=5,
            width=6,
            term=Terminal()
        ),}

        # Test data and state.
        msgs = [tm.Store('spam', exp['spam']),]

        # Run test and gather actual.
        self._send_msgs(msgs, 'test_store_display', False)
        act = self.displays

        # Determine test result.
        self.assertDictEqual(exp, act)

    def test_updates_display(self):
        """Sent a `log.Update` message, `queued_manager()` should
        route the message to the currently showing panel and print
        any resulting update.
        """
        # Expected value.
        exp = [
            call((
                f'{term.move(0, 0)}                    '
                f'{term.move(1, 0)}                    '
                f'{term.move(2, 0)}                    '
                f'{term.move(3, 0)}                    '
                f'{term.move(4, 0)}                    '
                f'{term.move(0, 0)}spam'
            ), end='', flush=True),
            call((
                f'{term.move(0, 0)}                    '
                f'{term.move(1, 0)}                    '
                f'{term.move(2, 0)}                    '
                f'{term.move(3, 0)}                    '
                f'{term.move(4, 0)}                    '
                f'{term.move(0, 0)}eggs'
                f'{term.move(1, 0)}spam'
            ), end='', flush=True),
        ]

        # Test data and state.
        p = log.Log(
            content=('spam',),
            height=5,
            width=20,
        )
        msgs = [
            tm.Store('spam', p),
            tm.Show('spam'),
            log.Update('eggs'),
        ]

        # Run test.
        act = self._send_msgs(msgs, 'test_updates_display', False)

        # Determine test result.
        self.assertEqual(exp, act)

    # Complex tests.
    @patch('blessed.Terminal.height', new_callable=PropertyMock)
    @patch('blessed.Terminal.width', new_callable=PropertyMock)
    @patch('blessed.Terminal.fullscreen')
    @patch('thurible.thurible.print')
    def test_change_terminal_dimensions_changes_panel_dimensions(
        self,
        mock_print,
        mock_fullscreen,
        mock_width,
        mock_height
    ):
        """When the size of the terminal changes and a fullscreen panel
        is showing, the size of the panel should be updated to match the
        new size of the terminal.
        """
        # Expected values.
        exp_before = {'height': 24, 'width': 80,}
        exp_after = {'height': 31, 'width': 43,}

        # Test data and state.
        mock_height.return_value = exp_before['height']
        mock_width.return_value = exp_before['width']
        msgs = [
            tm.Store('spam', splash.Splash('spam')),
            tm.Show('spam'),
        ]
        self.t.start()
        for msg in msgs:
            self.q_to.put(msg)
        _ = self._watch_for_pong('before_change')

        # Run test.
        act_before = {
            'height': self.displays['spam'].height,
            'width': self.displays['spam'].width,
        }
        mock_height.return_value = exp_after['height']
        mock_width.return_value = exp_after['width']
        _ = self._watch_for_pong('after_change')
        act_after = {
            'height': self.displays['spam'].height,
            'width': self.displays['spam'].width,
        }

        # Determine test result.
        self.assertEqual(exp_before, act_before)
        self.assertEqual(exp_after, act_after)

    @patch('blessed.Terminal.cbreak')
    @patch('blessed.Terminal.fullscreen')
    def test_terminal_modes(self, mock_fullscreen, mock_cbreak):
        """While running, the terminal should be in `fullscreen` and
        `cbreak` modes.
        """
        # Expected values.
        exp_fs = [call(), call().__enter__(),]
        exp_cb = [call(), call().__enter__(),]

        # Run test and gather actuals.
        self.t.start()
        _ = self._watch_for_pong('test_terminal_modes')
        act_fs = mock_fullscreen.mock_calls
        act_cb = mock_cbreak.mock_calls

        # Determine test result.
        self.assertEqual(exp_fs, act_fs)
        self.assertEqual(exp_cb, act_cb)
