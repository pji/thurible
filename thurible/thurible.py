"""
thurible
~~~~~~~~~~~

Managers for the data displays.
"""
from collections import deque
from dataclasses import dataclass
from queue import Queue
from typing import Optional

from blessed import Terminal

from thurible import messages as tm
from thurible.panel import Panel
from thurible.dialog import Dialog
from thurible.util import get_terminal


# Manager.
def queued_manager(
    q_to: Queue,
    q_from: Queue,
    term: Optional[Terminal] = None,
    displays: Optional[dict] = None
) -> None:
    """Manager for running the terminal display in a separate thread
    or process.

    Manage a terminal display by sending and receiving
    :class:`thurible.messages.Message` objects through
    :class:`queue.Queue` objects.

    :param q_to: A queue for messages the program sends to the manager.
    :param q_from: A queue for messages the manager sends to the program.
    :param term: An instance of `blessed.Terminal` used to interact with
        the terminal.
    :param displays: (Optional.) Storage for the panels the program may
        want the manager to display.
    :return: None.
    :rtype: NoneType

    Usage::

        >>> from queue import Queue
        >>> from threading import Thread
        >>> from thurible import get_terminal, queued_manager
        >>> from thurible.messages import End
        >>>
        >>> # Create a queue to send messages to the manager.
        >>> q_in = Queue()
        >>>
        >>> # Create a queue to receive messages from the manager.
        >>> q_out = Queue()
        >>>
        >>> # Get a terminal instance for the manager to use.
        >>> term = get_terminal()
        >>>
        >>> # Run the manager in a separate thread.
        >>> T = Thread(target=queued_manager, args=(q_in, q_out, term))
        >>> T.start()
        >>>
        >>> # End the thread running the queued_manager.
        >>> msg = End('Ending.')
        >>> q_in.put(msg)

    """
    # Set up.
    if term is None:
        term = get_terminal()
    if displays is None:
        displays = {}
    showing: str = ''
    history: deque[str] = deque(maxlen=100)
    farewell = ''
    reason = ''
    exception: Optional[Exception] = None
    last_height = term.height
    last_width = term.width

    # Program loop.
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        while True:
            if showing and displays[showing].height == last_height:
                if term.height != last_height:
                    displays[showing].height = term.height
                    last_height = term.height
                    print(term.clear, end='', flush=True)
                    print(str(displays[showing]), end='', flush=True)
            if showing and displays[showing].width == last_width:
                if term.width != last_width:
                    displays[showing].width = term.width
                    last_width = term.width
                    print(term.clear, end='', flush=True)
                    print(str(displays[showing]), end='', flush=True)

            try:
                (
                    displays, showing, end, farewell, reason, history
                ) = check_messages(
                    q_to,
                    q_from,
                    displays,
                    showing,
                    history
                )
                if end:
                    break
                check_input(q_from, displays, showing, term)

            except Exception as ex:
                reason = 'Exception.'
                exception = ex
                break

    # After exiting full screen mode, print the farewell message and
    # inform the program the manager is ending..
    if farewell:
        print(farewell)
    q_from.put(tm.Ending(reason, exception))


# Core functions.
def check_input(
    q_from: Queue,
    displays: dict[str, Panel],
    showing: str,
    term: Terminal
) -> None:
    """Check if input from the user was received and act on any
    received.
    """
    key = term.inkey(timeout=.01)
    if key:
        update = ''
        data = str(key)
        if showing and isinstance(displays[showing], Panel):
            data, update = displays[showing].action(key)
        if update:
            print(update, end='', flush=True)
        if data:
            msg = tm.Data(data)
            q_from.put(msg)


def check_messages(
    q_to: Queue,
    q_from: Queue,
    displays: dict[str, Panel],
    showing: str,
    history: deque[str]
) -> tuple[dict[str, Panel], str, bool, str, str, deque[str]]:
    """Check if messages from the program were received and act on any
    received.
    """
    end = False
    reason = ''
    farewell = ''
    if not q_to.empty():
        msg = q_to.get()
        if isinstance(msg, tm.End):
            farewell = msg.text
            reason = 'Received End message.'
            end = True
        elif isinstance(msg, tm.Ping):
            pong = tm.Pong(msg.name)
            q_from.put(pong)
        elif isinstance(msg, tm.Show):
            if showing:
                history.appendleft(showing)
            showing = msg.name
            print(str(displays[showing]), end='', flush=True)
        elif isinstance(msg, tm.Showing):
            shown = tm.Shown(msg.name, showing)
            q_from.put(shown)
        elif isinstance(msg, tm.Store):
            displays[msg.name] = msg.display
        elif isinstance(msg, tm.Delete):
            del displays[msg.name]
        elif isinstance(msg, tm.Storing):
            stored = tm.Stored(
                msg.name,
                tuple(key for key in displays)
            )
            q_from.put(stored)
        elif isinstance(msg, tm.Alert):
            height = len(get_terminal().wrap(
                msg.text,
                width=int(displays[showing].width * 0.6)
            ))
            rel_height = (height + 3) / displays[showing].height
            displays[msg.name] = Dialog(
                message_text=msg.text,
                options=msg.options,
                title_text=msg.title,
                frame_type='light',
                panel_align_h='center',
                panel_align_v='middle',
                panel_relative_height=rel_height,
                panel_relative_width=0.6,
                height=displays[showing].height,
                width=displays[showing].width
            )
            history.appendleft(showing)
            showing = msg.name
            print(str(displays[showing]), end='', flush=True)
        elif isinstance(msg, tm.Dismiss) and msg.name == showing:
            history.appendleft(showing)
            showing = history[1]
            print(str(displays[showing]), end='', flush=True)
        else:
            update = displays[showing].update(msg)
            if update:
                print(update, end='', flush=True)
    return displays, showing, end, farewell, reason, history
