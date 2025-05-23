.. Thurible documentation master file, created by
   sphinx-quickstart on Sun Dec 11 11:29:58 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

###############
:mod:`thurible`
###############

The :mod:`thurible` package provides tools for creating user interfaces
in terminal applications. It's built on top of the :mod:`blessed` package,
but no interaction with the :mod:`blessed` package is required. The
intention is for all interactions with terminal to be abstracted into
"panels" that are displayed to the user.

.. note::  
    A :dfn:`thurible` is a metal vessel hanging from chains used to burn
    incense during religious ceremonies. It seemed a reasonable name for
    a package build on top of :mod:`blessed`. Plus, it's just a fun word.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   self
   /panels.rst
   /managers.rst
   /messages.rst
   /utility.rst
   /updates.rst


.. _using:

Using :mod:`thurible`
*********************

:dfn:`Panels` format and display data in a terminal. If you are used
to working with graphical user interfaces, you can think of them like
windows. They are how the application puts data on the screen.

While :mod:`thurible` has tools for handling displaying panels for you,
you can display a panel yourself just by using :func:`print`. Let's
say you just want to put the word "SPAM" in the middle of the terminal::

    from thurible import Splash
    
    splash = Splash('spam')
    print(splash, end='', flush=True)

Do you have to add the :attr:`end` and :attr:`flush` attributes to the
:func:`print`? Yes. Or, at least, it works better if you do. Without
:attr:`end`, :func:`print` will add a new line after it prints the panel,
which will cause the top of the panel to scroll up off the top of the
terminal window. Without :attr:`flush`, :func:`print` may delay printing
the panel until there is more text to display in the terminal, causing
your panel to be displayed after it is relevant to the user.

Using :func:`print` to display the panel only shows the panel in the
terminal. It won't all users to interact with the panel by, for example,
scrolling through its text or selecting a menu option. While it's
possible to create your own code for handling that, the easiest way to
do it is to use a manager.


.. _advanced:

Managers and Messages
*********************

:dfn:`Managers` manage displaying panels and retrieving user input, so
you don't have to worry about it. Your code just needs to tell the
manager what you want to display and watch for messages back from the
manager containing input from the user.

:dfn:`Messages` are the objects you use to send instructions to the
manager, and they are the objects the manager uses to send data back
to you.

Let's expand on the previous example. You still want to put the word
"SPAM" in the middle of the screen. But, now, you want to end the
program after the user presses any key on their keyboard::

    from threading import Thread
    from thurible import get_queues, queued_manager, Splash
    import thurible.messages as tm

    # Set up and run the thread for the manager.
    q_to, q_from = get_queues()
    T = Thread(target=queued_manager, args=(q_to, q_from))
    T.start()

    # Create the panel.
    footer = 'Press any key to continue.'
    splash = Splash('spam', frame_type='heavy', footer=footer)

    # Tell the manager to display the panel.
    store = tm.Store('splash', splash)
    show = tm.Show('splash')
    q_to.put(store)
    q_to.put(show)

    # Watch for input indicating the user has pressed a key or if the
    # manager is ending for some other reason, meaning you'll never get
    # the key pressed by the user.
    data = None
    while not isinstance(data, [tm.Data, tm.Ending]):
        if not q_from.empty():
            data = q_from.get()
    
    # Once the user pressed a key, tell the manager to end gracefully.
    # If the manager sent an Ending message, then you don't need to
    # tell it to end. It's crashed on its own.
    if isinstance(data, tm.Data):
        end = tm.End('Goodbye!')
        q_to.put(end)


Usage Examples
**************
Usage examples are found in the `examples/` directory.

examples/eventsplash.py
    A terminal application that uses a :class:`thurible.event_manager`
    to display a simple splash screen.
examples/favword.py
    A terminal application that uses :mod:`thurible` to ask the user for
    their favorite word.
examples/filereader.py
    A terminal application that uses :mod:`thurible` to navigate the
    filesystem and read files.
examples/tensecs.py
    A terminal application that uses :mod:`thurible` to track a ten
    second wait using a progress bar.
examples/showsplash.py
    A terminal application that uses a :class:`thurible.queued_manager`
    to display a simple splash screen.


Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
