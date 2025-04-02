"""
test_eventmanager
~~~~~~~~~~~~~~~~~

Unit tests for the :mod:`thurible.eventmanager` module.
"""
from queue import Queue

import pytest as pt

import thurible.eventmanager as em
import thurible.messages as tm


# Fixtures.
@pt.fixture
def queues(mocker):
    q_from = Queue()
    q_to = Queue()
    mocker.patch(
        'thurible.eventmanager.get_queues',
        return_value=(q_to, q_from)
    )
    yield (q_to, q_from)


# Test case.
def test_events_invoked_by_messages(mocker, queues):
    """When the UI sends a message to the application,
    :func:`eventmanager.event_manager` sends that event to
    the callable mapped to that event.
    """
    values = {'p': tm.Ping('spam'), 'q': tm.End('Quit'),}

    def data(msg, q_to, values=values):
        q_to.put(values[msg.value])
        return not (msg.value == 'q')

    mocker.patch('thurible.eventmanager.Thread')
    q_to, q_from = queues
    event_map = {tm.Data: data,}
    for msg in [tm.Data('p'), tm.Data('q')]:
        q_from.put(msg)

    mgr = em.event_manager(event_map)
    assert q_to.get() == values['p']
    assert q_to.get() == values['q']
    assert q_to.empty()


def test_starts_queued_manager_and_ends(mocker, queues):
    """When invoked, :func:`eventmanager.event_manager` starts
    a :func:`thurible.queued_manager`. When that manager sends
    an :class:`thurible.messages.Ending` message, the event
    managers ends, too.
    """
    mocker.patch('thurible.eventmanager.Thread')
    q_to, q_from = queues
    q_from.put(tm.Ending('spam'))

    # The test is checking to make sure event_manager doesn't hang.
    # If it does, you should be able to ^C out of it.
    mgr = em.event_manager()
