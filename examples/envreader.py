"""
envreader
~~~~~~~~~
Display the current environment variables in a table.
"""
import os
from collections.abc import Generator
from dataclasses import dataclass
from queue import Queue

import thurible as thb
import thurible.messages as tm


# The rows in a thurible.Table have to be dataclass objects.
@dataclass
class EnvVar:
    """An environment variable."""
    name: str
    value: str


EnvVars = tuple[EnvVar, ...]


def get_envvars() -> EnvVars:
    """Get the current environment's variables."""
    return tuple(EnvVar(key, os.environ[key]) for key in os.environ)


# With thurible, actually displaying that panel will be taken care of
# by a manager. In this case, we are going to use the event_manager.
# The event_manager will display panels for you and react to input
# events from the user. To understand how to react, the event_manager
# needs "event handlers", functions you provide that act on the input
# events.
#
# Event handlers must meet the following criteria:
#
# * Accept a response message from the UI as a parameter.
# * Accept a queue for sending command messages to the UI as a parameter.
# * Return a bool that says whether the program should keep running.
#
# This event handler is designed to handle Data messages.
def data_handler(msg: tm.Message, q_to: Queue) -> bool:
    """Handle data messages."""
    # To keep mypy happy, double check to make sure you got a Data
    # message.
    if not isinstance(msg, tm.Data):
        raise TypeError(
            'This should only get Data messages. '
            f'Received {type(msg).__name__}.'
        )

    # We are going to end when the user presses any key, so any Data
    # message causes us to end the manager.
    #
    # Since we are ending the program, tell the UI to end. Otherwise,
    # it might try to keep running after everything else ends, which
    # is messy.
    q_to.put(tm.End(f'The "{msg.value}" key was pressed.'))

    # Now, tell the event_manager to end.
    return False


# This handler handles Ending messages. The event_handler will do this
# for you even if you don't give it an Ending handler, but giving it
# an Ending handler will allow you to customize that behavior.
def ending_handler(msg: tm.Message, q_to: Queue) -> bool:
    """Handle Ending messages."""
    # To keep mypy happy, double check to make sure you got an Ending
    # message.
    if not isinstance(msg, tm.Ending):
        raise TypeError('This should only get Ending messages.')

    # if the UI ran into an exception, raise that for the application.
    if msg.ex:
        raise msg.ex

    # Otherwise, just tell the event_manager to stop running.
    return False


# Construct and populate the table.
records = get_envvars()
table = thb.Table(
    records,
    frame_type='light',
    inner_frame=True,
    title_text='env'
)

# Now we map the event handlers to the messages they should respond to.
# Note that the handlers do not have parentheses after them. That's
# because we are mapping to the function itself. If you put parentheses
# after them, it will try to run the function right now, which isn't
# what we want.
event_map = {
    tm.Data: data_handler,
    tm.Ending: ending_handler,
}

# And the last step is to run the event_manager.
thb.event_manager(event_map, table)
