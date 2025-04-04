"""
test_thurible
~~~~~~~~~~~~~~~~

Unit tests for the `thurible.thurible` module.
"""
from collections.abc import Iterator
from queue import Queue
from threading import Thread
from time import sleep
from unittest.mock import PropertyMock, call

import pytest as pt

from thurible import dialog, log, menu
from thurible import messages as tm
from thurible import splash
from thurible import thurible as thb


# Fixtures.
@pt.fixture
def in_thread(queues, mocker):
    """The test runs in a thread."""
    mocker.patch('thurible.thurible.Terminal.fullscreen')
    q_to, q_from = queues
    displays = {}
    T = Thread(target=thb.queued_manager, kwargs={
        'q_to': q_to,
        'q_from': q_from,
        'displays': displays
    })
    yield T, q_to, q_from, displays
    if T.is_alive():
        q_to.put(tm.End())


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


def get_delayed_input(msgs, inputs, in_thread, mocker):
    mocker.patch('blessed.Terminal.fullscreen')
    mocker.patch('thurible.thurible.print')
    mocker.patch('blessed.Terminal.inkey', side_effect=inputs)
    mocker.patch('blessed.Terminal.cbreak')
    T, q_to, q_from, _ = in_thread
    for msg in msgs:
        if isinstance(msg, tm.Ping):
            ping_name = msg.name
    T.start()
    for msg in msgs:
        q_to.put(msg)
    resp = None
    count = 0
    while not resp:
        if not q_from.empty():
            msg = q_from.get()
            if isinstance(msg, tm.Pong) and msg.name == ping_name:
                inputs.on = True
            else:
                resp = msg
        assert count <= 100
        count += 1
        sleep(0.01)
    return resp


def get_msg_response(msgs, name, in_thread, mocker=None):
    T, q_to, q_from, _ = in_thread
    if mocker:
        mocker.patch('blessed.Terminal.fullscreen')
        mocker.patch('thurible.thurible.print')
    T.start()
    for msg in msgs:
        q_to.put(msg)
    resps = watch_for_pong(q_to, q_from, name=name)
    return resps


def send_msgs(msgs, name, in_thread, will_end=True):
    T, q_to, q_from, displays = in_thread
    T.start()
    for msg in msgs:
        q_to.put(msg)
    if not will_end:
        watch_for_pong(q_to, q_from, name=name)
    else:
        watch_for_pong(q_to, q_from, msg=tm.Ending('Received End message.'))


def watch_for_pong(q_to, q_from, name='', msg=None):
    """Send a ping to the queued_manager and wait for the pong
    response, collecting all responses received before the pong.
    This is usually done to ensure the queue_manager thread has
    had time to process all of the previous messages sent to it.
    """
    if not msg:
        msg = tm.Pong(name)
        q_to.put(tm.Ping(name))

    count = 0
    resp = None
    resps = []
    while resp != msg:
        if resp:
            resps.append(resp)
            if isinstance(resp, tm.Ending):
                break
            resp = None

        if not q_from.empty():
            resp = q_from.get()

        assert count <= 100
        count += 1
        sleep(.01)
    return resps


# Test cases.
class TestQueuedManager:
    def test_delete_display(self, capsys, in_thread):
        """Sent a Delete message, queued_manager() should delete the
        Panel with the given name from the stored panels.
        """
        msgs = [
            tm.Store('eggs', splash.Splash('eggs')),
            tm.Store('spam', splash.Splash('spam')),
            tm.Delete('eggs'),
        ]
        send_msgs(msgs, 'test_delete_display', in_thread, False)
        _, _, _, displays = in_thread
        assert displays == {'spam': splash.Splash('spam'),}

    def test_display_alert(self, capsys, in_thread, term):
        """Sent an Alert message, queued_manager() should display an
        alert panel over the top of the current panel. Sent a Dismiss
        message, queued_manager() should restore the current panel.
        """
        T, q_to, q_from, displays = in_thread
        s = splash.Splash(content='spam', height=10, width=30)
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
        send_msgs(msgs, 'test_display_alert', in_thread, False)
        captured = capsys.readouterr()
        assert captured.out == (
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
        )

    def test_get_display(self, capsys, in_thread):
        """Sent a `Showing` message, queued_manager() should return a
        `Shown` message with the currently displayed panel.
        """
        msgs = [
            tm.Store('spam', splash.Splash('eggs')),
            tm.Show('spam'),
            tm.Showing('test_get_display')
        ]
        result = get_msg_response(msgs, 'test_show_display', in_thread)
        assert result == [tm.Shown('test_get_display', 'spam'),]

    def test_list_stored_display(self, capsys, in_thread):
        """Sent a `Storing` message, queued_manager() should return a
        `Stored` message with a list of stored panels.
        """
        items = ('spam', 'eggs', 'bacon',)
        msgs = [tm.Store(item, splash.Splash(item)) for item in items]
        msgs.append(tm.Storing('ham'))
        result = get_msg_response(msgs, 'test_list_stored_display', in_thread)
        assert result == [tm.Stored('ham', items),]

    def test_print_farewell(self, capsys, in_thread):
        """Sent an End message with a farewell string, the farewell
        string should be printed as the queued_manager() terminates.
        """
        msgs = [tm.End('spam'),]
        send_msgs(msgs, 'test_print_farewell', in_thread)
        captured = capsys.readouterr()
        assert captured.out == 'spam\n'

    def test_sends_selection_from_menu(
        self, KEY_DOWN, KEY_ENTER, capsys, in_thread, menu_options, mocker
    ):
        """Receiving input from the user that isn't acted on by the
        display, `queued_manager()` should send the input to the
        application as a Data message.
        """
        msgs = [
            tm.Store('menu', menu.Menu(menu_options[:3], height=5, width=7)),
            tm.Show('menu'),
            tm.Ping('test_sends_selection_from_menu'),
        ]
        inputs = EndlessSideEffect([KEY_DOWN, KEY_ENTER], False)
        result = get_delayed_input(msgs, inputs, in_thread, mocker)
        assert result == tm.Data('eggs')

    def test_sends_exception(self, capsys, in_thread):
        """When an exception is raised in queued_manager, it sends the
        exception to the program and ends.
        """
        class Spam(splash.Splash):
            ex = ValueError('eggs')

            def __str__(self):
                raise self.ex

        msgs = [
            tm.Store('spam', Spam('spam', height=5, width=6)),
            tm.Show('spam')
        ]
        result = get_msg_response(msgs, 'test_sends_exception', in_thread)
        assert result == [tm.Ending('Exception.', Spam.ex),]

    def test_sends_input_to_application(
        self, KEY_X, capsys, in_thread, mocker
    ):
        """Receiving input from the user that isn't acted on by the'
        display, `queued_manager()` should send the input to the
        application as a Data message.
        """
        msgs = [
            tm.Store('spam', splash.Splash('spam', height=5, width=6)),
            tm.Show('spam'),
            tm.Ping('test_sends_input_to_application'),
        ]
        inputs = EndlessSideEffect([KEY_X,], False)
        result = get_delayed_input(msgs, inputs, in_thread, mocker)
        assert result == tm.Data('x')

    def test_show_display(self, capsys, in_thread, term):
        """Sent a Show message, queued_manager() should write the
        string to the terminal.
        """
        msgs = [
            tm.Store('spam', splash.Splash('spam', height=5, width=20)),
            tm.Show('spam')
        ]
        send_msgs(msgs, 'test_show_display', in_thread, False)
        captured = capsys.readouterr()
        assert captured.out == (
            f'{term.move(0, 0)}                    '
            f'{term.move(1, 0)}                    '
            f'{term.move(2, 0)}                    '
            f'{term.move(3, 0)}                    '
            f'{term.move(4, 0)}                    '
            f'{term.move(2, 8)}spam'
        )

    def test_store_display(self, capsys, in_thread):
        """Sent a Store message, queued_manager() should store the
        contained Display for later use.
        """
        msgs = [tm.Store('spam', splash.Splash('spam', height=5, width=6)),]
        send_msgs(msgs, 'test_store_display', in_thread, False)
        _, _, _, display = in_thread
        assert display == {'spam': splash.Splash('spam', height=5, width=6),}

    def test_updates_display(self, capsys, in_thread, term):
        """Sent a `log.Update` message, `queued_manager()` should
        route the message to the currently showing panel and print
        any resulting update.
        """
        msgs = [
            tm.Store('spam', log.Log(('spam',), height=5, width=20)),
            tm.Show('spam'),
            log.Update('eggs'),
        ]
        send_msgs(msgs, 'test_updates_display', in_thread, False)
        captured = capsys.readouterr()
        assert captured.out == (
            f'{term.move(0, 0)}                    '
            f'{term.move(1, 0)}                    '
            f'{term.move(2, 0)}                    '
            f'{term.move(3, 0)}                    '
            f'{term.move(4, 0)}                    '
            f'{term.move(0, 0)}spam'
            f'{term.move(0, 0)}                    '
            f'{term.move(1, 0)}                    '
            f'{term.move(2, 0)}                    '
            f'{term.move(3, 0)}                    '
            f'{term.move(4, 0)}                    '
            f'{term.move(0, 0)}eggs'
            f'{term.move(1, 0)}spam'
        )


class TestQueuedManagerComplex:
    @pt.mark.skip(reason='terminal_unsafe')
    def test_change_terminal_dimensions_changes_panel_dimensions(
        self, in_thread, mocker
    ):
        """When the size of the terminal changes and a fullscreen panel
        is showing, the size of the panel should be updated to match the
        new size of the terminal.
        """
        mock_height = mocker.patch(
            'thurible.thurible.Terminal.height',
            new_callable=PropertyMock,
            return_value=24
        )
        mock_width = mocker.patch(
            'thurible.thurible.Terminal.width',
            new_callable=PropertyMock,
            return_value=31
        )
        msgs = [
            tm.Store('spam', splash.Splash('spam')),
            tm.Show('spam'),
        ]
        T, q_to, q_from, displays = in_thread
        T.start()
        for msg in msgs:
            q_to.put(msg)
        watch_for_pong(q_to, q_from, 'before_change')
        assert displays['spam'].height == 24
        assert displays['spam'].width == 31

        mock_height.return_value = 80
        mock_width.return_value = 43
        watch_for_pong(q_to, q_from, 'after_change')
        assert displays['spam'].height == 80
        assert displays['spam'].width == 43

    def test_terminal_modes(self, capsys, in_thread, mocker):
        """While running, the terminal should be in `fullscreen` and
        `cbreak` modes.
        """
        mock_cbreak = mocker.patch('blessed.Terminal.cbreak')
        mock_fscreen = mocker.patch('blessed.Terminal.fullscreen')
        T, q_to, q_from, _ = in_thread
        T.start()
        watch_for_pong(q_to, q_from, 'test_terminal_modes')
        assert mock_cbreak.mock_calls == [call(), call().__enter__(),]
        assert mock_fscreen.mock_calls == [call(), call().__enter__(),]
