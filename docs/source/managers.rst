.. _managers:

########
Managers
########

:dfn:`Managers` manage displaying panels and retrieving user input, so
you don't have to worry about it. Your code just needs to tell the
manager what you want to display and watch for messages back from the
manager containing input from the user.

.. autofunction:: thurible.queued_manager
.. autofunction:: thurible.event_manager


.. manager-ops:

How Managers Work
*****************
The following are details on the internal operations of managers to
help you understand how to work with them. While they apply to both
managers, these details are mostly hidden from :func:`event_manager`.
It's more important to understand them when working with
:func:`queued_manager`.


.. _manager-loop:

The Manager Loop
^^^^^^^^^^^^^^^^
Once started, a manager loops through a standard set of actions until
it is told to close or crashes. Those actions are:

#.  Check for a message from the application.

    #.  If there was a comand message, perform the commanded action.
    #.  If the commanded action should return a response to the
        application, send that response.
    #.  If there is no action for the command message received, send
        that message to the :meth:`Panel.update` of the currently
        displayed panel.

#.  Check for a key press from the user.

    #.  If there was a key press, send the
        :class:`blessed.keyboard.Keystroke` object to the
        :meth:`Panel.action` of the currently displayed panel.
    #.  If the :meth:`Panel.action` returns data, send that data
        to the application in a :class:`thurible.messages.Data`
        message.
    #.  If the :meth:`Panel.action` returns an update, print
        that update to the terminal.

The loop will end under the following conditions:

*   The application sends a :class:`thurible.messages.End` message,
*   The manager encounters a known exception it cannot recover from.
*   The manager encounters an unknown exception.

When possible, the manager will send a :class:`thurible.messages.Ending`
message to announce the end of the loop. If the loop is ending due to
and exception, that exception is passed to the application within
the :class:`thurible.messages.Ending` message.


.. _storing-panels:

Storing Panels
^^^^^^^^^^^^^^
To allow your application to pre-load panels and easily switch back
and forth between panels without having to recreate them, the
manager stores all panels sent to it with the
:class:`thurible.messages.Store` message or created with the
:class:`thurible.messages.Alert` message. Those messages allow you
to assign a name to the panel, which is then used by other messages,
like :class:`thurible.messages.Show`, to interact with the stored
panels.

.. warning::
    Managers store panels in a :class:`dict` object, using the
    name given to the panel as the key. This means that if you
    provide the same name for two panels, one panel will overwrite
    the other panel. For this reason, it is recommended all panels
    be given unique names.


.. mgr_examples:

Examples
^^^^^^^^
The `examples` directory in the :mod:`thurible` repository provides
examples for how to use managers.

An example of using :func:`event_manager` is found in:

*   `examples/eventsplash.py`

Examples of using :func:`queued_manager` are found in:

*   `examples/favword.py`
*   `examples/filereader.py`
*   `examples/showsplash.py`
*   `examples/tensecs.py`
