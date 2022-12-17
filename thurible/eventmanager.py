"""
eventmanager
~~~~~~~~~~~~

A manager that uses events sent from the user interface to drive
application flow.
"""
from queue import Queue
from threading import Thread
from typing import Callable, Optional

from thurible import queued_manager, get_queues
import thurible.messages as tm


# Manager.
def event_manager(event_map: Optional[dict[str, Callable]] = None) -> str:
    """Manages a terminal UI based on events coming from the UI."""
    if not event_map:
        event_map = {}

    q_to, q_from = get_queues()
    T = Thread(target=queued_manager, args=(q_to, q_from))
    run = True

    try:
        T.start()
        while run:
            run = _check_for_message(q_to, q_from, event_map)

    except KeyboardInterrupt as ex:
        reason = 'Keyboard Interrupt'
        msg = tm.End(reason)
        q_to.put(msg)
        raise ex


def _check_for_message(
    q_to: Queue,
    q_from: Queue,
    event_map: dict[str, Callable]
) -> bool:
    """Check for and handle UI messages."""
    run = True
    if not q_from.empty():
        msg = q_from.get()
        if isinstance(msg, tm.Ending):
            run = False
    return run
