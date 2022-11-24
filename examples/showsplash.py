"""
showsplash
~~~~~~~~~~

Display a splash screen in the terminal.
"""
from queue import Queue
from threading import Thread
from typing import Optional

import thurible as thb
import thurible.messages as tm


if __name__ == '__main__':
    # Since thurible.queue_manager is designed to be used in a separate
    # thread or process, there needs to be shared queues to allow the
    # program to send commands to the manager and the manager to send
    # input and data back to the program.
    q_to = Queue()
    q_from = Queue()

    # This creates an instance of blessed.Terminal that the panels will
    # use to interact with the terminal. Your code does not need to
    # interact with the blessed package at all. Though, it is imported
    # as a dependency of thurible.
    term = thb.get_terminal()

    # In thurible, a manager is used to send output to the terminal
    # and to receive input from the user. For showsplash, we are using
    # the queued_manager, which is designed to be run in a separate
    # threat or process from the rest of your application. That way,
    # interaction with the terminal will not block the running of your
    # code and vice versa.
    #
    # Create the thread used to run queued_manager and start it.
    T = Thread(target=thb.queued_manager, args=(q_to, q_from, term))
    T.start()

    # thurible displays output in the terminal through panels. Input
    # from the user will also be send to the currently active panel
    # before it is sent to your code. This is to allow some simple
    # navigation functions to be built into the panel, so you don't
    # have to worry about it.
    #
    # In this case we are using the Splash panel, which will show a
    # "splash screen" to the user.
    splash = thb.Splash(

        # This is the text that will be displayed in the splash screen.
        content='SPAM!',

        # Panels in thurible fill an area within the terminal. The
        # current version requires you give the explicit height and
        # width of that area. The height is measured in rows, and the
        # width is measured in columns. Since we want the splash to
        # fill the entire terminal, we are using the blessed.Terminal
        # object from earlier to get the height and width of the
        # terminal.
        height=term.height,
        width=term.width,

        # The last of the required panel parameters is term. It needs
        # an instance of blessed.Terminal that the panel will use to
        # interact with the terminal.
        term=term
    )

    # The program interacts with the manager by sending it Messages.
    #
    # The Store message tells the manager to store a panel with a
    # name that you can use in future messages to the manager. This
    # allows you to preload panels in the manager, showing them only
    # when you need.
    store_msg = tm.Store('spam', splash)

    # The Show message tells the manager to display the panel with the
    # given name in the terminal. This panel will then also be the
    # first to receive all input from the user.
    show_msg = tm.Show('spam')

    # Since the manager is running in a separate thread, you cannot
    # communicate to it directly. Messages need to be added to the
    # queue that sends messages to the manager.
    q_to.put(store_msg)
    q_to.put(show_msg)

    # Since the manager is running on a separate thread, it cannot
    # communicate directly with you. You need to watch the queue that
    # receives messages from the manager for messages. In this case,
    # we want to watch for two things: user input or a message from
    # manager saying it's ending on its own. User input will be sent
    # in a Data message. The manager should send an Ending message
    # before it ends. So, we are just going to watch the queue for
    # either of those messages.
    msg_from: Optional[tm.Message] = None
    while not isinstance(msg_from, (tm.Data, tm.Ending)):
        if not q_from.empty():
            msg_from = q_from.get()

    # The End message tells the queued_manager to end. This should
    # terminate the thread cleanly from within. Again, since the
    # manager is in a separate thread, the message has to be sent
    # using the queue that sends messages to the manager.
    end_msg = tm.End('Goodbye message.')
    q_to.put(end_msg)
