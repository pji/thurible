.. _panels:

######
Panels
######

:dfn:`Panels` format and display data in a terminal. If you are used
to working with graphical user interfaces, you can think of them like
windows. They are how the application puts data on the screen.

.. _interfaces:

Common Interfaces
*****************

In :mod:`thurible`, a panel is a subclass of :class:`thurible.panel.Panel.`
That class and a couple additional protocols define much of the common
behavior of panel objects.

For more details on how panels are sized within the terminal, see
:ref:`sizing`.

For more details on how to define how panels react to user input,
see :ref:`active`.

.. autoclass:: thurible.panel.Panel
    :members:
.. autoclass:: thurible.panel.Frame
    :members:
.. autoclass:: thurible.panel.Content
    :members:
.. autoclass:: thurible.panel.Scroll
    :members:
.. autoclass:: thurible.panel.Title
    :members:

.. _defined-panels:

Defined Panels
**************

The following panels are made available by :mod:`thurible` to cover common
use cases.

.. autoclass:: thurible.Dialog
    :members:
.. autoclass:: thurible.Log
    :members:
.. autoclass:: thurible.Menu
    :members:
.. autoclass:: thurible.Progress
    :members:
.. autoclass:: thurible.Splash
    :members:
.. autoclass:: thurible.Text
    :members:
.. autoclass:: thurible.TextDialog
    :members:

.. _sizing:

Sizing Panels
*************

Panels attempt to allow for the relative sizing of an element
within a terminal. What does that mean?

A terminal window has a size in rows and columns. These rows
and columns are measured in relation to a fixed-width character.
A row is the height of one character. A column is the width of
one character. For reasons that go back to the era of punch
cards and hardware terminals, the common default size of a
terminal window is 24 rows by 80 columns.

However, terminal widows do not have to be that standard size.
Most terminal emulators that I've used allow you to set any
size you want for the size of the terminal window, and you can
resize the window after you open it. That creates a problem if
you are trying to create a consistent interface for a terminal
application. Sure, you can usually assume that a terminal is
going to be 24×80, but if you run into a terminal that is
48×132, things might get weird.

Panel tries to solve that by allowing you to set the size of
a panel relative to the terminal window, no matter what size
that terminal window is. Now, there are some limitation to that.
If the terminal window is 1×1, there isn't much that can be
shown in that terminal. However, it still should be useful for
most terminal sizes you are going to run into.

.. _absolute:

The Absolute Sizing Model
-------------------------
To position the panel in the terminal, :mod:`thurible` managers start
with the absolute position. The absolute position is determined
by the following attributes:

height
    The number of rows from the top of the panel to the bottom.
    If you don't specify a height, it will default to the
    total number of rows in the current terminal window.
width
    The number of columns from the left side of the panel to
    the right side. If you don't specify a width, it will
    default to the number of columns in the current terminal
    window.
origin_x
    The left-most column of the panel. If you don't specify an
    origin_x, it will default to the left-most row of the
    terminal window.
origin_y
    The top-most row of the panel. If you don't specify an
    origin_y, it will default to the top-most row of the
    terminal window.

For the most part, it's best not to set these manually, and just
let it default to fill the entire terminal window. However, if
you have some case where you need to manually set them, such as
simplifying unit tests, you can do so.

.. _relative:

The Relative Sizing Model
-------------------------
After determining the absolute position of the panel, :mod:`thurible`
then uses the following attributes to determine where the
interior space of the panel is located relative to the absolute
position of the panel in the terminal window.

The horizontal positioning attributes are:

*	panel_pad_left
*   panel_relative_width
*   panel_pad_right

The vertical positioning attributes are:

*   panel_pad_top
*   panel_relative_height
*   panel_pad_bottom

Each of those takes a value from 0.0 to 1.0, inclusive, that
sets what percentage of the absolute size of the panel is
taken up by that part of the relative size. For example, let's
say you create the following panel::

    panel = Panel(
        origin_x=0,
        width=80,
        panel_pad_left=0.2
    )

The absolute left side of the panel is the left-most column of
the terminal window (in Python that's referred to as column 0,
those curses programming will often call it column 1). The
absolute width of the terminal is 80 columns. However, the
interior of the frame starts 20% of the total width of the panel
from the absolute left-most column, which is column::

    80 * 0.2 = 16

The interior then takes of the remaining 80% of the absolute
width of the panel, or::

    80 * 0.8 = 64

As shown in the example, you do not need to set all three of
the relative positioning attribute for each dimension. In most
cases, it's only necessary to set one per dimension.

.. note::
    If you do set all three of the relative positioning
    attributes for a dimension, you must ensure that the sum
    of all three attributes equals 1.0. Because floating-point
    math is involved, it's theoretically possible that some
    values that look like they should add to 1.0 won't add to
    1.0. The best way to avoid that is never set all three
    of the attributes for a dimension. Set one, or at most
    two, and let the panel object calculate the rest for you.

While you can set any of the three relative positional
attributes, it is recommended that you use ones that set the
relative interior sizes:

*   panel_relative_height
*   panel_relative_width

Then, instead of setting any of the "panel_pad" attributes, set
the alignment attribute for the dimension:

*   panel_align_h
*   panel_align_v

Setting those attributes will align the relative interior area
of the panel with the absolute area of the panel.

The valid values when setting panel_align_h are:

*   left
*   center
*   right

The valid values when setting panel_align_v are:

*   top
*   middle
*   bottom

For example, if you create the following panel::

    panel = Panel(
        panel_relative_height=0.25,
        panel_relative_width=0.25,
        panel_align_h='right',
        panel_align_v='bottom'
    )

You will get a panel that will fill the bottom-right quarter of
the terminal window.

.. note::
    You cannot set panel alignment attributes (panel_align_h
    and panel_align_v) and the panel padding attributes (any of
    the panel_pad_* attributes) at the same time. The alignment
    attributes use the panel padding attributes to position the
    interior of the panel, so setting both of them would create
    a conflict that could lead to unexpected behavior.

.. _active:

Active Keys
***********

An :dfn:`active key` is a keyboard key that, when pressed by the user,
will be intercepted and handled by the panel rather than passed on to
the application.

An :dfn:`action handler` is a method that accepts a key press, as
represented by a :class:`blessed.keyboard.Keystroke` object returned
by :meth:`blessed.Terminal.inkey.` It defines the behavior of the panel
when the key is pressed, and it returns a :class:`str` with any updates
that need to be made to the terminal display.

The :mod:`thurible` library displays data to the user of a terminal
application. In some cases, the user needs to navigate within that
data. For example, the text displayed by a panel may be longer than
the number of rows in the current terminal window, so the user needs
to scroll down in the text to read all of it. Given a menu of options
the user needs to select the option they want. :mod:`Thurible` panels
will handle this sort of navigation for you through these active keys
and action handlers.

.. note::
    Active keys do not send any data back to your application. It's
    not intended for your application to even be aware they were
    pressed. Any input that needs to go back to your application
    should be handled in :meth:`Panel.action` and returned as the data
    :class:`str.`
