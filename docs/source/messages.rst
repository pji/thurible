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

.. class:: thurible.messages.Alert(name='alert', title='', text='Error.', \
    options=:obj:`thurible.dialog.cont`)
    
    Create a new :class:`thurible.messages.Alert` object. This
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

.. class:: thurible.messages.Delete(name)

    Create a new :class:`thurible.messages.Delete` object. This
    object is a command message used to instruct a manager to
    delete a stored panel.
    
    :param name: The name of the panel to delete.
    :return: None.
    :rtype: NoneType

.. class:: thurible.messages.Dismiss(name='alert')

    Create a new :class:`thurible.messages.Dismiss` object. This
    object is a command message used to stop displaying an alert.
    
    :param name: (Optional.) The name of the panel to dismiss.
    :return: None.
    :rtype: NoneType

.. class:: thurible.messages.End(text='')

    Create a new :class:`thurible.messages.End` object. This
    object is a command message used to instruct a manager to
    end the manager loop and quit.
    
    :param text: (Optional.) A message to print for the user after
        the manager loop ends.
    :return: None.
    :rtype: NoneType

.. class:: thurible.messages.Ping(name)

    Create a new :class:`thurible.messages.Ping` object. This
    object is a command message used to instruct a manager to
    reply with a :class:`thurible.message.Pong` message, proving
    the manager is still listening for and responding to messages.
    
    :param name: A unique name used to identify the resulting
        :class:`thurible.message.Pong` message as being caused
        by this message.
    :return: None.
    :rtype: NoneType

.. class:: thurible.messages.Show(name)

    Create a new :class:`thurible.messages.Show` object. This
    object is a command message used to instruct a manager to
    display a stored panel.
    
    :param name: The name of the panel to display.
    :return: None.
    :rtype: NoneType

.. class:: thurible.messages.Showing(name='')

    Create a new :class:`thurible.messages.Showing` object. This
    object is a command message used to instruct a manager to
    respond with a :class:`thurible.messages.Shown` message
    with the name of the currently displayed panel.
    
    :param name: (Optional.) A unique name used to identify the
        resulting :class:`thurible.message.Shown` message as being
        caused by this message.
    :return: None.
    :rtype: NoneType

.. class:: thurible.messages.Store(name, display)

    Create a new :class:`thurible.messages.Store` object. This
    object is a command message used to instruct a manager to
    store a panel for later display.
    
    :param name: The name of the panel to store.
    :param name: The panel to store.
    :return: None.
    :rtype: NoneType

.. class:: thurible.messages.Storing(name='')

    Create a new :class:`thurible.messages.Storing` object. This
    object is a command message used to instruct a manager to
    respond with a :class:`thurible.message.Stored` object
    containing the names of the currently stored panels.
    
    :param name: (Optional.) A unique name used to identify the
        resulting :class:`thurible.message.Stored` message as being
        caused by this message.
    :return: None.
    :rtype: NoneType

.. class:: thurible.log.Update(text)

    Create a new :class:`thurible.log.Update` object. This
    object is a command message used to instruct the currently
    displayed :class:`thurible.Log` to add the text given in the
    message.
    
    :param text: The message to add to the panel.
    :return: None.
    :rtype: NoneType

.. _response-messages:

Response Messages
*****************

.. class:: thurible.messages.Data(value)

    Create a new :class:`thurible.messages.Data` object. This
    object is a response message used to send data back to the
    application.
    
    :param value: The data being sent to the application.
    :return: None.
    :rtype: NoneType

.. class:: thurible.messages.Ending(reason='', ex=None)

    Create a new :class:`thurible.messages.Ending` object. This
    object is a response message used to inform the application
    that the manager is ending.
    
    :param reason: (Optional.) The reason the manager loop is
        ending.
    :param ex: (Optional.) The exception causing the manager
        loop to end.
    :return: None.
    :rtype: NoneType

.. class:: thurible.messages.Pong(name)

    Create a new :class:`thurible.messages.Pong` object. This
    object is a response message used to respond to a
    :class:`thurible.messages.Ping` message.
    
    :param name: The name of the :class:`thurible.messages.Ping`
        message that caused this response.
    :return: None.
    :rtype: NoneType

.. class:: thurible.messages.Shown(name, display)

    Create a new :class:`thurible.messages.Shown` object. This
    object is a response message used to respond to a
    :class:`thurible.messages.Showing` message.
    
    :param name: The name of the :class:`thurible.messages.Showing`
        message that caused this response.
    :param display: The name of the panel being displayed when the
        :class:`thurible.messages.Showing` was received.
    :return: None.
    :rtype: NoneType

.. class:: thurible.messages.Stored(name, stored)

    Create a new :class:`thurible.messages.Stored` object. This
    object is a response message used to respond to a
    :class:`thurible.messages.Storing` message.
    
    :param name: The name of the :class:`thurible.messages.Storing`
        message that caused this response.
    :param display: The names of the panel being stored when the
        :class:`thurible.messages.Storing` message was received.
    :return: None.
    :rtype: NoneType
