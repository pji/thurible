"""
messages
~~~~~~~~

Classes for communicating with `thurible` managers.
"""
from dataclasses import dataclass
from typing import Optional, Sequence

from thurible.dialog import cont
from thurible.menu import Option
from thurible.panel import Panel


# Base class.
class Message:
    """A base class to allow all messages to be identified."""


# Messages.
@dataclass
class Alert(Message):
    """Display an alert dialog to the user."""
    name: str = 'alert'
    title: str = ''
    text: str = 'Error.'
    options: Sequence[Option] = cont


@dataclass
class Data(Message):
    """Input from the user."""
    value: str


@dataclass
class Delete(Message):
    """Delete a stored panel."""
    name: str


@dataclass
class Dismiss(Message):
    """Dismiss an alert dialog displayed tp the user."""
    name: str = 'alert'


@dataclass
class End(Message):
    """Terminate the manager."""
    text: str = ''


@dataclass
class Ending(Message):
    """The manager announcing it is ending, usually a response to an
    End message.
    """
    reason: str = ''
    ex: Optional[Exception] = None


@dataclass
class Ping(Message):
    """Have the manager return a message saying this message was
    reached.
    """
    name: str


@dataclass
class Pong(Message):
    """Respond to a Ping message."""
    name: str


@dataclass
class Show(Message):
    """Show a stored display in the terminal."""
    name: str


@dataclass
class Showing(Message):
    """Query for the key for the currently shown display in the
    terminal.
    """
    name: str = ''


@dataclass
class Shown(Message):
    """The answer to the Showing query."""
    name: str
    display: str


@dataclass
class Store(Message):
    """Store a display for later use."""
    name: str
    display: Panel


@dataclass
class Stored(Message):
    """The response to a Storing message, containing the list the names
    of the stored panels.
    """
    name: str
    stored: tuple[str, ...]


@dataclass
class Storing(Message):
    """Query for the names of stored panels."""
    name: str = ''
