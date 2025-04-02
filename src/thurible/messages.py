"""
messages
~~~~~~~~

Classes for communicating with `thurible` managers.
"""
from dataclasses import dataclass
from typing import Optional, Sequence

from thurible.dialog import cont
from thurible.menu import Option
from thurible.panel import Message, Panel


# Command messages.
@dataclass
class Alert(Message):
    """Create a new :class:`thurible.messages.Alert` object. This
    object is a command message used to instruct a manager to
    show an alert message to the user.

    :param name: (Optional.) The name the manager will use to store
        the :class:`thurible.Dialog` object created in response to
        this message. The default name is "alert".
    :param title: (Optional.) The title of the alert.
    :param text: (Optional.) The text of the alert. The default value
        is "Error."
    :param options: (Optional.) The options given to the user for
        responding to the alert. The default is "Continue".
    :return: None.
    :rtype: NoneType
    """
    name: str = 'alert'
    title: str = ''
    text: str = 'Error.'
    options: Sequence[Option] = cont


@dataclass
class Delete(Message):
    """Create a new :class:`thurible.messages.Delete` object. This
    object is a command message used to instruct a manager to
    delete a stored panel.

    :param name: The name of the panel to delete.
    :return: None.
    :rtype: NoneType
    """
    name: str


@dataclass
class Dismiss(Message):
    """Create a new :class:`thurible.messages.Dismiss` object. This
    object is a command message used to stop displaying an alert.

    :param name: (Optional.) The name of the panel to dismiss.
    :return: None.
    :rtype: NoneType
    """
    name: str = 'alert'


@dataclass
class End(Message):
    """Create a new :class:`thurible.messages.End` object. This
    object is a command message used to instruct a manager to
    end the manager loop and quit.

    :param text: (Optional.) A message to print for the user after
        the manager loop ends.
    :return: None.
    :rtype: NoneType
    """
    text: str = ''


@dataclass
class Ping(Message):
    """Create a new :class:`thurible.messages.Ping` object. This
    object is a command message used to instruct a manager to
    reply with a :class:`thurible.message.Pong` message, proving
    the manager is still listening for and responding to messages.

    :param name: A unique name used to identify the resulting
        :class:`thurible.message.Pong` message as being caused
        by this message.
    :return: None.
    :rtype: NoneType
    """
    name: str


@dataclass
class Show(Message):
    """Create a new :class:`thurible.messages.Show` object. This
    object is a command message used to instruct a manager to
    display a stored panel.

    :param name: The name of the panel to display.
    :return: None.
    :rtype: NoneType
    """
    name: str


@dataclass
class Showing(Message):
    """Create a new :class:`thurible.messages.Showing` object. This
    object is a command message used to instruct a manager to
    respond with a :class:`thurible.messages.Shown` message
    with the name of the currently displayed panel.

    :param name: (Optional.) A unique name used to identify the
        resulting :class:`thurible.message.Shown` message as being
        caused by this message.
    :return: None.
    :rtype: NoneType
    """
    name: str = ''


@dataclass
class Store(Message):
    """Create a new :class:`thurible.messages.Store` object. This
    object is a command message used to instruct a manager to
    store a panel for later display.

    :param name: The name of the panel to store.
    :param name: The panel to store.
    :return: None.
    :rtype: NoneType
    """
    name: str
    display: Panel


@dataclass
class Storing(Message):
    """Create a new :class:`thurible.messages.Storing` object. This
    object is a command message used to instruct a manager to
    respond with a :class:`thurible.message.Stored` object
    containing the names of the currently stored panels.

    :param name: (Optional.) A unique name used to identify the
        resulting :class:`thurible.message.Stored` message as being
        caused by this message.
    :return: None.
    :rtype: NoneType
    """
    name: str = ''


# Response messages.
@dataclass
class Data(Message):
    """Create a new :class:`thurible.messages.Data` object. This
    object is a response message used to send data back to the
    application.

    :param value: The data being sent to the application.
    :return: None.
    :rtype: NoneType
    """
    value: str


@dataclass
class Ending(Message):
    """Create a new :class:`thurible.messages.Ending` object. This
    object is a response message used to inform the application
    that the manager is ending.

    :param reason: (Optional.) The reason the manager loop is
        ending.
    :param ex: (Optional.) The exception causing the manager
        loop to end.
    :return: None.
    :rtype: NoneType
    """
    reason: str = ''
    ex: Optional[Exception] = None


@dataclass
class Pong(Message):
    """Create a new :class:`thurible.messages.Pong` object. This
    object is a response message used to respond to a
    :class:`thurible.messages.Ping` message.

    :param name: The name of the :class:`thurible.messages.Ping`
        message that caused this response.
    :return: None.
    :rtype: NoneType
    """
    name: str


@dataclass
class Shown(Message):
    """Create a new :class:`thurible.messages.Shown` object. This
    object is a response message used to respond to a
    :class:`thurible.messages.Showing` message.

    :param name: The name of the :class:`thurible.messages.Showing`
        message that caused this response.
    :param display: The name of the panel being displayed when the
        :class:`thurible.messages.Showing` was received.
    :return: None.
    :rtype: NoneType
    """
    name: str
    display: str


@dataclass
class Stored(Message):
    """Create a new :class:`thurible.messages.Stored` object. This
    object is a response message used to respond to a
    :class:`thurible.messages.Storing` message.

    :param name: The name of the :class:`thurible.messages.Storing`
        message that caused this response.
    :param display: The names of the panel being stored when the
        :class:`thurible.messages.Storing` message was received.
    :return: None.
    :rtype: NoneType
    """
    name: str
    stored: tuple[str, ...]
