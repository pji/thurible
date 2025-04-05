########
thurible
########

Tools for creating fullscreen terminal UIs on top of blessed.


What does it do?
================
It provides some tools for creating and managing interactive user
interfaces in the terminal.


Why Did I Make This?
====================
I have a couple of programs that have interactive UIs in a terminal,
and I wanted to consolidate that code. There are probably other packages
that do this better, but I prefer to keep my dependencies to a minimum.
Plus, I like playing with terminal user interfaces. They're neat.


Will It Work with My Terminal?
==============================
It's intended to work with anything that `blessed` works with. Is
that everything? Probably not. Certainly some features, like color,
will only work if your terminal supports it. Some things, like the
frames that can go around the panels rely on Unicode characters that
may not exist in all fonts. If you're using a variable width font in
your terminal… I don't know. Things are probably going to be messed up.

If you run into something should work but isn't, open an issue. I'm
just doing this on my own in my spare time, but I'll try to look at it.


Using `thurible`
================
`Panels` format and display data in a terminal. If you are used
to working with graphical user interfaces, you can think of them like
windows. They are how the application puts data on the screen.

While `thurible` has tools for handling displaying panels for you,
you can display a panel yourself just by using `print`. Let's
say you just want to put the word "SPAM" in the middle of the terminal::

    from thurible import Splash
    
    splash = Splash('spam')
    print(splash, end='', flush=True)

Do you have to add the `end` and `flush` attributes to the
`print`? Yes. Or, at least, it works better if you do. Without
`end`, `print` will add a new line after it prints the panel,
which will cause the top of the panel to scroll up off the top of the
terminal window. Without `flush`, `print` may delay printing
the panel until there is more text to display in the terminal, causing
your panel to be displayed after it is relevant to the user.

Using `print` to display the panel only shows the panel in the
terminal. It won't all users to interact with the panel by, for example,
scrolling through its text or selecting a menu option. While it's
possible to create your own code for handling that, the easiest way to
do it is to use a manager.


Managers and Messages
=====================
`Managers` manage displaying panels and retrieving user input, so
you don't have to worry about it. Your code just needs to tell the
manager what you want to display and watch for messages back from the
manager containing input from the user.

`Messages` are the objects you use to send instructions to the
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
==============
Usage examples are found in the `examples/` directory.

examples/eventsplash.py
    A terminal application that uses a `thurible.event_manager`
    to display a simple splash screen.
examples/favword.py
    A terminal application that uses `thurible` to ask the user for
    their favorite word.
examples/filereader.py
    A terminal application that uses `thurible` to navigate the
    filesystem and read files.
examples/tensecs.py
    A terminal application that uses `thurible` to track a ten
    second wait using a progress bar.
examples/showsplash.py
    A terminal application that uses a `thurible.queued_manager`
    to display a simple splash screen.

