###########
thurible
###########

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


How Do I Use It?
================
There are three key parts of `thurible` to understand:

*   Panels: these create the UI seen in the terminal.
*   Managers: these run the UI in a separate thread and return data to
    your code.
*   Messages: these are used to pass messages from your code to a
    manager.


Panels
------
`Panel` objects do the following:

*   Store data to be displayed in the terminal,
*   Generate the text to display in the terminal,
*   Respond to navigation input from the user.

While you can create your own custom `Panel` objects, there are several
subclasses in `thurible` that may cover basic needs:

*   `Menu`: a menu of options a user can select from.
*   `Splash`: a splash screen.
*   `Table`: a simple table for viewing dataclasses.
*   `Text`: a simple text display.

If you use a manager with a pre-built `Panel`, it will handle passing
input to and getting output from the `Panel` for you. If you aren't
using a manager or are creating a custom `Panel`, there are two core
features of `Panel` object to be aware of:

*   Getting a string representation of a `Panel` object, such as by
    using the `str()` function, will return all of the content of the
    `Panel` complete with the terminal escape codes needed to redraw
    the entire `Panel` with a simple `print()` function.
*   Passing keyboard input, as a `blessed.Keystroke` object, into the
    `action()` method of the `Panel` will return a `tuple` of two
    values:
    
    *   data: If the `Panel` doesn't know what to do with the `Keystroke`,
        the string value of the `Keystroke` will be returned here.
    *   update: If the `Panel` needs to make changes to the terminal due
        to the `Keystroke`, these changes will be returned here as a
        string that can be passed to a simple `print()` function.

.. note::
    Despite the name, `Panel` objects do not create curses-style panels
    in the terminal. As far as I'm aware, the `blessed` package doesn't
    offer the capability of creating those kinds of panels. However, the
    idea is, eventually, for `thurible` to provide that type of
    functionality on top of `blessed`.


Managers
--------
Manager functions do the following:

*   Receive output from the program to display in the terminal.
*   Make any needed updates to the terminal.
*   Send input from the user to the program.

There is currently only one pre-built manager function: `queued_manager`.


Messages
--------
Communication to and from a manager is done with defined "messages."
These messages are the dataclasses found in `thurible.thurible`.

Programs can send the following messages to a manager:

`Alert(name, title, text, options)`
    Tell the manager to display an alert dialog.
`Dismiss`
    Tell the manager to dismiss the alert dialog.
`End(text)`
    Tell the manager to terminate.
`Ping(name)`
    Tell the manager to respond with a `Pong` message.
`Show(name)`
    Tell the manager to switch to displaying the named `Panel`.
`Showing()`
    Ask the manager for the name of the currently displayed `Panel`.
`Store(name, panel)`
    Tell the manager to store the given `Panel` as the given name for
    future display.

The manager can send the following message to the program:

`Data(value)`
    Contains input received from the user.
`Ending(reason, exception)`
    Announces the manager is terminating.
`Pong(name)`
    Is the response to a `Ping` message from the program.
`Shown(name)`
    Is the response to a `Showing` message from the program, containing
    the name of the currently displayed `Panel`.


Usage Example
-------------
Usage examples are found in the `examples/` directory.

examples/filereader.py
    A terminal application that uses `thurible` to navigate the
    filesystem and read files.
examples/showsplash.py
    A terminal application that uses `thurible` to display a simple
    splash screen.

If you want to run them to see what they do, you need to run them like
modules. For example, to run filereader from the root of the repository,
run the following::

    python3 -m examples.filereader

To-Do List
==========
The following items are still needed before initial release:

*   Add documentation.
*   Manager updates:
    *   Allow unrecognized messages from programs to go to panels.
    *   Allow managers to catch sigkill and pass it on to the program.
    *   Add coroutine manager.
*   Panel updates:
    *   Allow panels to react to messages sent by managers.
    *   Add a logging panel.
    *   Add a progress panel.
    *   Add a textfield panel.
    *   Add a textform panel.
    *   Add a tableform panel.
