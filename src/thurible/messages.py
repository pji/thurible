"""
.. _messages:

########
Messages
########

:dfn:`Messages` are the objects you use to send instructions to the
manager, and they are the objects the manager uses to send data back
to you.


.. _command-messages:

Command Messages
****************
These messages should be used by your application to control the
manager running the terminal display. They should never be sent
by the manager to the application.

.. autoclass:: thurible.messages.Alert
.. autoclass:: thurible.messages.Delete
.. autoclass:: thurible.messages.Dismiss
.. autoclass:: thurible.messages.End
.. autoclass:: thurible.messages.Ping
.. autoclass:: thurible.messages.Show
.. autoclass:: thurible.messages.Showing
.. autoclass:: thurible.messages.Store
.. autoclass:: thurible.messages.Storing
.. autoclass:: thurible.Update
.. autoclass:: thurible.Tick
.. autoclass:: thurible.NoTick


.. _response-messages:

Response Messages
*****************
These messages are used by managers to respond to or alert your
application. They should never be sent by the application to the
manager.

.. autoclass:: thurible.messages.Data
.. autoclass:: thurible.messages.Ending
.. autoclass:: thurible.messages.Pong
.. autoclass:: thurible.messages.Shown
.. autoclass:: thurible.messages.Stored

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
    :return: An :class:`thurible.messages.Alert` object.
    :rtype: thurible.messages.Alert
    :usage:
        To create a :class:`thurible.messages.Alert` object:

        .. testcode:: alert

            import thurible.messages as msgs
            from thurible.menu import Option

            name = 'alert1'
            title = 'Warning'
            text = 'Something broke.'
            option_1 = Option('Panic', 'p')
            option_2 = Option('Flee', 'f')
            options = [option_1, option_2]
            msg = msgs.Alert(name, title, text, options)

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
    :return: An :class:`thurible.messages.Delete` object.
    :rtype: thurible.messages.Delete
    :usage:
        To create a :class:`thurible.messages.Delete` object:

        .. testcode::

            import thurible.messages as msgs

            name = 'alert1'
            msg = msgs.Delete(name)

    """
    name: str


@dataclass
class Dismiss(Message):
    """Create a new :class:`thurible.messages.Dismiss` object. This
    object is a command message used to stop displaying an alert.

    :param name: (Optional.) The name of the panel to dismiss.
    :return: An :class:`thurible.messages.Dismiss` object.
    :rtype: thurible.messages.Dismiss
    :usage:
        To create a :class:`thurible.messages.Dismiss` object:

        .. testcode::

            import thurible.messages as msgs

            name = 'alert1'
            msg = msgs.Dismiss(name)

    """
    name: str = 'alert'


@dataclass
class End(Message):
    """Create a new :class:`thurible.messages.End` object. This
    object is a command message used to instruct a manager to
    end the manager loop and quit.

    :param text: (Optional.) A message to print for the user after
        the manager loop ends.
    :return: An :class:`thurible.messages.End` object.
    :rtype: thurible.messages.End
    :usage:
        To create a :class:`thurible.messages.End` object:

        .. testcode::

            import thurible.messages as msgs

            name = 'Goodbye!'
            msg = msgs.End(name)

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
    :return: An :class:`thurible.messages.Ping` object.
    :rtype: thurible.messages.Ping
    :usage:
        To create a :class:`thurible.messages.Ping` object:

        .. testcode::

            import thurible.messages as msgs

            name = 'ping1'
            msg = msgs.Ping(name)

    """
    name: str


@dataclass
class Show(Message):
    """Create a new :class:`thurible.messages.Show` object. This
    object is a command message used to instruct a manager to
    display a stored panel.

    :param name: The name of the panel to display.
    :return: An :class:`thurible.messages.Show` object.
    :rtype: thurible.messages.Show
    :usage:
        To create a :class:`thurible.messages.Show` object:

        .. testcode::

            import thurible.messages as msgs

            name = 'alert1'
            msg = msgs.Show(name)

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
    :return: An :class:`thurible.messages.Showing` object.
    :rtype: thurible.messages.Showing
    :usage:
        To create a :class:`thurible.messages.Showing` object:

        .. testcode::

            import thurible.messages as msgs

            name = 'alert1'
            msg = msgs.Showing(name)

    """
    name: str = ''


@dataclass
class Store(Message):
    """Create a new :class:`thurible.messages.Store` object. This
    object is a command message used to instruct a manager to
    store a panel for later display.

    :param name: The name of the panel to store.
    :param display: The panel to store.
    :return: An :class:`thurible.messages.Store` object.
    :rtype: thurible.messages.Store
    :usage:
        To create a :class:`thurible.messages.Store` object:

        .. testcode::

            import thurible.messages as msgs
            from thurible import Dialog

            name = 'alert1'
            dialog = Dialog('Be alerted!')
            msg = msgs.Store(name, dialog)

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
    :return: An :class:`thurible.messages.Storing` object.
    :rtype: thurible.messages.Storing
    :usage:
        To create a :class:`thurible.messages.Storing` object:

        .. testcode::

            import thurible.messages as msgs

            name = 'check_stored_displays'
            msg = msgs.Storing(name)

    """
    name: str = ''


# Response messages.
@dataclass
class Data(Message):
    """Create a new :class:`thurible.messages.Data` object. This
    object is a response message used to send data back to the
    application.

    :param value: The data being sent to the application.
    :return: An :class:`thurible.messages.Data` object.
    :rtype: thurible.messages.Data
    :usage:
        To create a :class:`thurible.messages.Data` object:

        .. testcode::

            import thurible.messages as msgs

            name = 'datum'
            msg = msgs.Data(name)

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
    :return: An :class:`thurible.messages.Ending` object.
    :rtype: thurible.messages.Ending
    :usage:
        To create a :class:`thurible.messages.Ending` object:

        .. testcode::

            import thurible.messages as msgs

            name = 'keyboard interrupt'
            ex = KeyboardInterrupt
            msg = msgs.Ending(name, ex)

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
    :return: An :class:`thurible.messages.Pong` object.
    :rtype: thurible.messages.Pong
    :usage:
        To create a :class:`thurible.messages.Pong` object:

        .. testcode::

            import thurible.messages as msgs

            name = 'pong1'
            msg = msgs.Pong(name)

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
    :return: An :class:`thurible.messages.Shown` object.
    :rtype: thurible.messages.Shown
    :usage:
        To create a :class:`thurible.messages.Shown` object:

        .. testcode::

            import thurible.messages as msgs

            name = 'check_display'
            display = 'alert1'
            msg = msgs.Shown(name, display)

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
    :return: An :class:`thurible.messages.Stored` object.
    :rtype: thurible.messages.Stored
    :usage:
        To create a :class:`thurible.messages.Stored` object:

        .. testcode::

            import thurible.messages as msgs

            name = 'check_stored_displays'
            stored = ['alert1', 'text1', 'doc_menu', 'text2',]
            msg = msgs.Stored(name, stored)

    """
    name: str
    stored: tuple[str, ...]
