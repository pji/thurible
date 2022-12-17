"""
eventmanager
~~~~~~~~~~~~

A manager that uses events sent from the user interface to drive
application flow.
"""
from queue import Queue
from threading import Thread
from typing import Callable, Optional

from thurible.panel import Panel
from thurible.thurible import queued_manager
from thurible.util import get_queues
import thurible.messages as tm


# Manager.
def event_manager(
    event_map: Optional[dict[type, Callable]] = None,
    initial_panel: Optional[Panel] = None
) -> None:
    """Manage a terminal display by mapping :ref:`response-messages`
    to functions in your application.

    :param event_map: (Optional.) A :class:`dict` mapping the
        :class:`thurible.panel.Message` types managers can send to
        applications (:ref:`response-messages`) to functions in
        your application. These functions must accept a
        :class:`queue.Queue` object and the response message as
        parameters. It must return a :class:`bool` indicating
        whether the application should continue running.
    :param initial_panel: (Optional.) The first panel displayed in
        the terminal. While this is technically optional, that's
        just for testing purposes. You should really provide
        this to the manager. The panel passed this way will be
        stored as "__init".
    :return: None
    :rtype: NoneType

    Usage::

        from thurible import event_manager, Splash
        import thurible.messages as tm

        # Create the event handlers.
        def data_handler(msg, q_to):
            msg = tm.End('Quitting.')
            q_to.put(msg)
            return False

        def ending_handler(msg, q_to):
            if msg.exception:
                raise msg.exception
            return False

        # Map the handlers to event messages.
        event_map = {
            tm.Data: data_handler,
            tm.Ending: ending_handler,
        }

        # Create the panel to display when the manager starts.
        splash = Splash('SPAM!')

        # Run the event_manager.
        event_manager(event_map, splash)
    """
    if not event_map:
        event_map = {}

    q_to, q_from = get_queues()
    T = Thread(target=queued_manager, args=(q_to, q_from))
    run = True

    try:
        T.start()
        if initial_panel:
            q_to.put(tm.Store('__init', initial_panel))
            q_to.put(tm.Show('__init'))

        while run:
            run = _check_for_message(q_to, q_from, event_map)

    except KeyboardInterrupt as ex:
        reason = 'Keyboard Interrupt'
        msg = tm.End(reason)
        q_to.put(msg)
        raise ex


# Private functions.
def _check_for_message(
    q_to: Queue,
    q_from: Queue,
    event_map: dict[type, Callable]
) -> bool:
    """Check for and handle UI messages."""
    run = True
    if not q_from.empty():
        msg = q_from.get()

        for msg_type in event_map:
            if isinstance(msg, msg_type):
                run = event_map[msg_type](msg, q_to)
                break
        else:
            if isinstance(msg, tm.Ending):
                run = False
    return run
