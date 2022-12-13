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
.. autoclass:: thurible.log.Update
.. autoclass:: thurible.progress.Tick

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
