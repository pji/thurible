"""
thurible
~~~~~~~~~~~

Managers for the data displays.
"""
from dataclasses import dataclass
from queue import Queue
from typing import Optional

from blessed import Terminal

from thurible.panel import Panel
from thurible import messages as tm


def queued_manager(
    q_to: Queue,
    q_from: Queue,
    term: Terminal,
    displays: Optional[dict] = None
) -> None:
    """Manager for running the terminal display in a separate thread
    or process.

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
    if displays is None:
        displays = {}
    showing: str = ''
    farewell = ''
    ending_reason = ''
    exception: Optional[Exception] = None

    # Program loop.
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        while True:
            try:
                if not q_to.empty():
                    msg = q_to.get()
                    if isinstance(msg, tm.End):
                        farewell = msg.text
                        ending_reason = 'Received End message.'
                        break
                    elif isinstance(msg, tm.Ping):
                        pong = tm.Pong(msg.name)
                        q_from.put(pong)
                    elif isinstance(msg, tm.Show):
                        showing = msg.name
                        print(str(displays[showing]), end='', flush=True)
                    elif isinstance(msg, tm.Showing):
                        shown = tm.Shown(showing)
                        q_from.put(shown)
                    elif isinstance(msg, tm.Store):
                        displays[msg.name] = msg.display

                key = term.inkey(timeout=.01)
                if key:
                    acted = False
                    update = ''
                    data = str(key)
                    if showing and isinstance(displays[showing], Panel):
                        data, update = displays[showing].action(key)
                    if update:
                        print(update, end='', flush=True)
                    if data:
                        msg = tm.Data(data)
                        q_from.put(msg)

            except Exception as ex:
                ending_reason = 'Exception.'
                exception = ex
                break

    # After exiting full screen mode, print the farewell message and
    # inform the program the manager is ending..
    if farewell:
        print(farewell)
    q_from.put(tm.Ending(ending_reason, exception))
