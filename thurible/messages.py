"""
messages
~~~~~~~~

Classes for communicating with `thurible` managers.
"""
from dataclasses import dataclass
from typing import Optional

from thurible.panel import Panel


# Base class.
class Message:
    """A base class to allow all messages to be identified."""


# Messages.
@dataclass
class Data(Message):
    """Input from the user."""
    value: str


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


@dataclass
class Shown(Message):
    """The answer to the Showing query."""
    name: str


@dataclass
class Store(Message):
    """Store a display for later use."""
    name: str
    display: Panel
