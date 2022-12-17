"""
test_eventmanager
~~~~~~~~~~~~~~~~~

Unit tests for the :mod:`thurible.eventmanager` module.
"""
from queue import Queue
from unittest.mock import call, patch

from tests.test_panel import term, TerminalTestCase
from thurible import queued_manager
import thurible.eventmanager as em
import thurible.messages as tm


# Test case.
class EventManagerTestCase(TerminalTestCase):
    def setUp(self):
        self.q_to = Queue()
        self.q_from = Queue()

    @patch('thurible.eventmanager.Thread')
    @patch('thurible.eventmanager.get_queues')
    def test_starts_queued_manager_and_ends(self, mock_qs, mock_thread):
        """When invoked, :func:`eventmanager.event_manager` starts
        a :func:`thurible.queued_manager`. When that manager sends
        an :class:`thurible.messages.Ending` message, the event
        managers ends, too.
        """
        # Expected values.
        exp = [
            call(target=queued_manager, args=(self.q_to, self.q_from)),
            call().start,
        ]

        # Test data and state.
        mock_qs.return_value = self.q_to, self.q_from
        self.q_from.put(tm.Ending('spam'))

        # Run test.
        mgr = em.event_manager()

        # Gather actual values.
        act = mock_thread.mock_calls

        # Determine test results.
        self.assertEqual(exp, act)
