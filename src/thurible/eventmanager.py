"""
eventmanager
~~~~~~~~~~~~

A manager that uses events sent from the user interface to drive
application flow.
"""
from queue import Queue
from threading import Thread
from typing import Callable, Mapping, Optional

import thurible.messages as tm
from thurible.panel import Panel
from thurible.thurible import queued_manager
from thurible.util import get_queues


# Types.
EventScript = Callable[[tm.Message, Queue], bool]
EventMap = Mapping[type, EventScript]


# Manager.
def event_manager(
    event_map: Optional[EventMap] = None,
    initial_panel: Optional[Panel] = None
) -> None:
    """Manage a terminal display by mapping :ref:`response-messages`
    to event scripts (see below).

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
    :usage:
        An example small application that uses the
        :func:`thurible.event_manager` show a splash
        screen then quit if a button is pressed::

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

    :event scripts:
        An :dfn:`event script` is a function that:

            *   Accepts a :ref:`response message<response-messages>`
                it will receive from the manager and a
                :class:`queue.Queue` for it to send
                :ref:`command messages<command-messages>`
                to the manager.
            *   Returns `True` if the manager should continue
                running.
            *   Returns `False` if the manager should end.

        For example, let's say we want an event script that will
        handle user input. It will:

            *   Display a splash screen if the user presses `x`,
            *   Display a different splash screen if the user
                presses `y`,
            *   End the :func:`event_manager` if the user presses
                the space bar.

        That would look like::

            import thurible
            from thurible import messages as msgs

            def data_handler(data, q_to):
                keep_running = True

                # If the user presses `x` display the X screen.
                if data.value == 'x':
                    splash = thurible.Splash('XXXXX')
                    store_msg = msgs.Store('x', splash)
                    q_to.put(store_msg)
                    show_msg = msgs.Show('x')
                    q_to.put(show_msg)

                # If the user presses `y` display the Y screen.
                if data.value == 'y':
                    splash = thurible.Splash('YYYYY')
                    store_msg = msgs.Store('y', splash)
                    q_to.put(store_msg)
                    show_msg = msgs.Show('y')
                    q_to.put(show_msg)

                # If the user presses ` ` end.
                if data.value == ' ':
                    keep_running = False

                return keep_running

        These event scripts are intended for fairly simple use
        cases. They respond to a single message from the manager.
        They can add messages to the manager's input queue to
        tell the manager to act. They can tell the manager to
        end.

        If you need more complex behaviors like checking the
        manager's state or maintaining internal state, you
        probably should use :func:`queued_manager` directly
        rather than :func:`event_manager`.

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
    event_map: EventMap
) -> bool:
    """Check for and handle UI messages."""
    run = True
    if not q_from.empty():
        msg = q_from.get()

        for msg_type in event_map:
            if isinstance(msg, msg_type) and isinstance(msg, tm.Message):
                run = event_map[msg_type](msg, q_to)
                break
        else:
            if isinstance(msg, tm.Ending):
                run = False
    return run
