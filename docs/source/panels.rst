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
that terminal window is. Now, there are some limitations to that.
If the terminal window is 1×1, there isn't much that can be
shown in that terminal. However, it still should be useful for
most terminal sizes you are going to run into.

.. _position_onion:

The Positioning Onion
---------------------

While it varies a little depending upon what classes a panel
inherits, there are generally four layers of positioning that
can happen within a panel:

*   Absolute
*   Frame (requires inheriting from :class:`thurible.panel.Frame`)
*   Inner
*   Content (requires inheriting from :class:`thurible.panel.Content`)

.. _absolute-layer:

The Absolute Layer
^^^^^^^^^^^^^^^^^^

The absolute layer is the first layer, and it is tracked in the
following attributes:

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

.. note::
    While you can set these manually, doing so will prevent the
    panel from being resized when the terminal is resized. The
    only intended use case for setting these is to simplify
    the writing of unit tests. In all other cases, it's recommended
    to allow these to default to the full size of the terminal
    window and use other parameters to position the panel.

.. _frame-layer:

The Frame Layer
^^^^^^^^^^^^^^^

For subclasses of :class:`thurible.panel.Frame`, the next layer in
positions the panel's frame. It's tracked by the following properties:

frame_height
    The number of rows from the top of the panel's frame to the bottom.
frame_width
    The number of columns from the left side of the panel's frame to
    the right side.
frame_x
    The left-most column of the panel's frame.
frame_y
    The top-most row of the panel's frame.

These are properties, so they cannot be set directly. You have to use
relative positioning attributes to affect these. That is done with
the attributes described in the :ref:`inner-layer` below.

.. _inner-layer:

The Inner Layer
^^^^^^^^^^^^^^^

The next positioning layer is the :dfn:`inner layer`. It's tracked
by the following properties:

inner_height
    The number of rows from the top of the panel's interior to the
    bottom.
inner_width
    The number of columns from the left side of the panel's
    interior to the right side.
inner_x
    The left-most column of the panel's interior.
inner_y
    The top-most row of the panel's interior.

These are properties, so they cannot be set directly. You have to
use the following attributes to set their value:

panel_relative_height
    The proportional height of the interior of the panel as
    compared to the absoute height of the panel. The proportion
    is given a :class:`float` with a value between 0.0 and 1.0,
    inclusive.
panel_relative_width
    The proportional width of the interior of the panel as
    compared to the absoute width of the panel. The proportion
    is given a :class:`float` with a value between 0.0 and 1.0,
    inclusive.
panel_align_h
    The horizontal alignment of the interior of the panel within
    the absolute width of the panel. The alignment is given as
    one of the following strings: "left", "center", or "right".
panel_align_v
    The vertical alignment of the interior of the panel within
    the absolute height of the panel. The alignment is given
    as one of the following strings: "top", "middle", "bottom".

.. note::
    There are two additional attributes that are involved:
    `panel_pad_left` and `panel_pad_right`. While it is
    currently possible to set these yourself, that
    ability will likely be removed in future versions. It
    is recommended to avoid using these two attributes.

So how does this actually work? Let's say we have the following
panel:

.. testcode::

    import thurible

    panel = thurible.panel.Panel(
        origin_x=0,
        width=80,
        panel_relative_width=0.8,
        panel_align_h='right'
    )

The width of the interior of the panel, as given by
:attr:`panel.inner_width` is:

.. testsetup:: inner_layer

    import thurible

    panel = thurible.panel.Panel(
        origin_x=0,
        width=80,
        panel_relative_width=0.8,
        panel_align_h='right'
    )

.. testcode:: inner_layer

    int(panel.width * panel.panel_relative_width) == 64
    int(80 * 0.8) == 64
    int(64.0) == 64

Since the interior is aligned "right", the starting point of the
interior, as given by :attr:`panel.inner_x` is:

.. testcode:: inner_layer

    panel.origin_x + (panel.width - panel.inner_width) == 16
    0 + (80 - 64) == 16
    0 + 16 == 16

Had the alignment been "center", it would have been:

.. testcode:: inner_layer

    panel.origin_x + (panel.width - panel.inner_width) // 2 == 8
    0 + (80 - 64) // 2 == 8
    0 + 16 // 2 == 8
    0 + 8 == 8

Had the alignment been "left", it would have been:

.. testcode:: inner_layer

    panel.origin_x == 0

.. warning::
    The above is not completely accurate for the current version
    of :mod:`thurible`. Instead, the panel uses
    :attr:`panel.panel_relative_width` to calculate the values of
    :attr:`panel.panel_pad_left` and :attr:`panel.panel_pad_right`.
    It then uses those values to determine the values for the
    `inner_*` attributes. However, the explanation above should
    be close to the results provided by the actual method, and
    future versions of :mod:`thurible` should move to the model
    described above.

.. note::
    In subclasses of :class:`thurible.panel.Frame`, adding a
    frame will affect the values of the `inner_*` attributes.
    The frame shrinks the interior by one character on each side
    of the interior. Therefore, if there had been a frame in the
    example above, :attr:`panel.inner_width` would have been 62
    and the :attr:`panel.inner_x` would've been 17.

.. _content-layer:

The Content Layer
^^^^^^^^^^^^^^^^^

For subclasses of :class:`thurible.panel.Content`, the next layer in
positions the panel's content. It's tracked by the following properties:

content_width
    The number of columns from the left side of the panel's content
    to the right side.
content_x
    The left-most column of the panel's content.

These are properties, so they cannot be set directly. You have to
use the following attributes to set their value:

content_relative_width
    The proportional width of the content of the panel as
    compared to the inner width of the panel. The proportion
    is given a :class:`float` with a value between 0.0 and 1.0,
    inclusive.
content_align_h
    The horizontal alignment of the content of the panel within
    the inner width of the panel. The alignment is given as
    one of the following strings: "left", "center", or "right".

.. note::
    There are two additional attributes that are involved:
    `content_pad_left` and `content_pad_right`. While it is
    currently possible to set these yourself, that
    ability will likely be removed in future versions. It
    is recommended to avoid using these two attributes.

These attributes work similar to the relative width and alignment
attributes in :ref:`inner-layer` above.

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
