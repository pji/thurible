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

In :mod:thurible, a panel is a subclass of :class:thurible.panel.Panel.
That class and a couple additional protocols define much of the common
behavior of panel objects.

.. class:: thurible.panel.Panel(height=None, width=None, term=None, \
                                origin_y=None, origin_x=None, bg='', \
                                fg='', panel_pad_bottom=None, \
                                panel_pad_left=None, panel_pad_right=None,\
                                panel_pad_top=None, \
                                panel_relative_height=None \
                                panel_relative_width=None \
                                panel_align_h=None, panel_align_v=None)

    Create a new :class:Panel object. This class serves as a parent
    class for all panels, providing the core code relating to the 
    area the panel fills in the terminal window.

    :param height: (Optional.) The height of the pane.
    :param width: (Optional.) The width of the pane.
    :param term: (Optional.) A :class:blessed.Terminal instance for
        formatting text for terminal display.
    :param origin_y: (Optional.) The terminal row for the top of the
        panel.
    :param origin_x: (Optional.) The terminal column for the left
        side of the panel.
    :param fg: (Optional.) A string describing the foreground color
        of the pane. See the documentation for :mod:blessed for more
        detail on the available options.
    :param bg: (Optional.) A string describing the background color
        of the pane. See the documentation for :mod:blessed for more
        detail on the available options.
    :param panel_pad_top: (Optional.) Distance between the
        Y origin of the panel and the top of the interior of the
        panel. It is a percentage expressed as a :class:float
        between 0.0 and 1.0, inclusive. See Sizing below for more
        information.
    :param panel_relative_height: (Optional.) The height of the
        interior of the panel in comparison of the full `height` of
        the panel. It is a percentage expressed as a :class:float
        between 0.0 and 1.0, inclusive. See Sizing below for more
        information.
    :param panel_pad_bottom: (Optional.) Distance between the
        full height of the panel and the interior of the panel.
        It is a percentage expressed as a :class:float between 0.0
        and 1.0, inclusive. See Sizing below for more information.
    :param panel_pad_left: (Optional.) Distance between the
        X origin of the panel and the left side of the interior
        of the panel. It is a percentage expressed as a :class:float
        between 0.0 and 1.0, inclusive. See Sizing below for more
        information.
    :param panel_relative_width: (Optional.) The width of the
        interior of the panel in comparison of the full width of
        the panel. It is a percentage expressed as a :class:float
        between 0.0 and 1.0, inclusive. See Sizing below for more
        information.
    :param panel_pad_right: (Optional.) Distance between the full
        width of the panel and the right side of the interior of
        the panel. It is a percentage expressed as a :class:float
        between 0.0 and 1.0, inclusive. See Sizing below for more
        information.
    :param panel_align_h: (Optional.) If the interior of the panel
        is smaller than the full width of the panel, this sets
        how the interior of the panel is aligned within the full
        height. It is a percentage expressed as a :class:float
        between 0.0 and 1.0, inclusive. See Sizing below for more
        information.
    :param panel_align_v: (Optional.) If the interior of the panel
        is smaller than the full width of the panel, this sets
        how the interior of the panel is aligned within the full
        height. It is a percentage expressed as a :class:float
        between 0.0 and 1.0, inclusive. See Sizing below for more
        information.
    :return: None.
    :rtype: NoneType

.. property:: Panel.active_keys

    The key presses the class will react to and the handler that
    acts on that key press.
    
    :return: A :class:dict object where the keys are the representation
        of the :class:blessed.keyboard.Keystroke object emitted when
        the key is pressed and the values are the action handler
        methods called when the key is pressed.
    :rtype: dict

.. property:: Panel.inner_height

    The number of rows in the terminal contained within the interior
    of the panel.
    
    :return: :class:int
    :rtype: int

.. property:: Panel.inner_width

    The number of columns in the terminal contained within the
    interior of the panel.
    
    :return: :class:int
    :rtype: int

.. property:: Panel.inner_x

    The left-most column in the terminal of the interior of the panel.
    
    :return: :class:int
    :rtype: int

.. property:: Panel.inner_y

    The top-most row in the terminal of the interior of the panel.
    
    :return: :class:int
    :rtype: int

.. method:: Panel.action(key)

    Act on a keystroke typed by the user.
    
    :param key: A :class:blessed.keyboard.Keystroke object representing
        the key pressed by the user.
    :return: A :class:tuple object containing two :class:str objects.
        The first string is any data that needs to be sent to the
        application. The second string contains any updates needed
        to be made to the terminal display.
    :rtype: tuple

.. method:: Panel.clear_contents()

    Clear the interior area of the panel.
    
    :return: A :class:str object containing the update needed to be
        made to the terminal display.
    :rtype: str

.. method:: Panel.register_key(key, handler)

    Declare the key presses the class will react to, and define the
    action the class will take when that key is pressed.
    
    :param key: The name of the key pressed as returned by the
        representation of the :class:blessed.keyboard.Keystroke
        emitted by the key press.
    :param handler: And action handler to invoke when the key is
        pressed. An action handler is a function that takes an
        optional :class:blessed.keyboard.Keystroke object and
        returns a string that contains any changes that need to be
        made to the terminal display as a result of the key press.
    :return: None.
    :rtype: NoneType

.. method:: Panel.update(msg)

    Act on a message sent by the application.
    
    :param msg: A message sent by the application.
    :return: A :class:str object containing any updates needed to be
        made to the terminal display.
    :rtype: str

.. _sizing:

Sizing Panels
=============

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
To position the panel in the terminal, :mod:thurible managers start
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
After determining the absolute position of the panel, :mod:thurible
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

.. note:
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

.. note:
    You cannot set panel alignment attributes (panel_align_h
    and panel_align_v) and the panel padding attributes (any of
    the panel_pad_* attributes) at the same time. The alignment
    attributes use the panel padding attributes to position the
    interior of the panel, so setting both of them would create
    a conflict that could lead to unexpected behavior.

.. _active:

Active Keys
===========

An :dfn:`active key` is a keyboard key that, when pressed by the user,
will be intercepted and handled by the panel rather than passed on to
the application.

An :dfn:`action handler` is a method that accepts a key press, as
represented by a :class:blessed.keyboard.Keystroke object returned
by :meth:blessed.Terminal.inkey. It defines the behavior of the panel
when the key is pressed, and it returns a :class:str with any updates
that need to be made to the terminal display.

The :mod:thurible library displays data to the user of a terminal
application. In some cases, the user needs to navigate within that
data. For example, the text displayed by a panel may be longer than
the number of rows in the current terminal window, so the user needs
to scroll down in the text to read all of it. Given a menu of options
the user needs to select the option they want. :mod:Thurible panels
will handle this sort of navigation for you through these active keys
and action handlers.

.. note:
    Active keys do not send any data back to your application. It's
    not intended for your application to even be aware they were
    pressed. Any input that needs to go back to your application
    should be handled in :meth:Panel.action and returned as the data
    :class:str.

.. class:: thurible.panel.Frame(frame_type=None, frame_bg='', frame_fg='' \
                                *args, **kwargs)

    Create a new :class:thurible.panel.Frame object. This class serves
    as a parent class for all panels that can have a frame surrounding
    the interior of the panel. As a subclass of :class:thurible.panel.Panel,
    it can also take those parameters and has those public methods.

    :param frame_type: (Optional.) If a string, the string determines
        the frame used for the pane. The available options are defined
        by :class:thurible.util.Box. If None, the pane doesn't have a
        frame.
    :param frame_fg: (Optional.) A string describing the foreground
        color of the frame. See the documentation for :mod:blessed for
        more detail on the available options. If :param:fg is set and
        this is not, the frame will have the :param:fg color.
    :param frame_bg: (Optional.) A string describing the background
        color of the frame. See the documentation for :mod:blessed for
        more detail on the available options. If :param:bg is set and
        this is not, the frame will have the :param:bg color.
    :return: None.
    :rtype: NoneType

.. class:: thurible.panel.Content(content_align_h='center', \
                                  content_align_v='middle', \
                                  content_pad_left=0.0, \
                                  content_pad_right=0.0, *args, **kwargs)

    Create a new :class:thurible.panel.Content object. This class
    serves as a parent class for all panels that allow padding between
    the frame surrounding the interior of the panel and the content
    contained by the panel. The nature of that content is defined by
    the subclass. As a subclass of :class:thurible.panel.Frame, it
    can also take those parameters and has those public methods.

    :param content_align_h: (Optional.) The horizontal alignment
        of the contents of the panel. It defaults to center.
    :param content_align_v: (Optional.) The vertical alignment of
        the contents of the penal. It defaults to middle.
    :param content_pad_left: (Optional.) The amount of padding
        between the left inner margin of the panel and the content.
        It is measured as a float between 0.0 and 1.0, where 0.0
        is no padding and 1.0 is the entire width of the panel is
        padding. The default is 0.0.
    :param content_pad_right: (Optional.) The amount of padding
        between the right inner margin of the panel and the content.
        It is measured as a float between 0.0 and 1.0, where 0.0
        is no padding and 1.0 is the entire width of the panel is
        padding. The default is 0.0.
    :return: None.
    :rtype: NoneType

.. class:: thurible.panel.Scroll(*args, **kwargs)

    Create a new :class:thurible.panel.Scroll object. This class
    serves as a parent class for all panels that allow the user
    to scroll through content that overflows the interior of the
    panel. As a subclass of :class:thurible.panel.Content, it can
    also take those parameters and has those public methods.
    
    This class defines the following active keys:
    
    *   KEY_END: Scroll to the end of the content.
    *   KEY_DOWN: Scroll down in the content.
    *   KEY_HOME: Scroll to the top of the content.
    *   KEY_PGDOWN: Scroll one screen down in the content.
    *   KEY_PGUP: Scroll one page up in the content.
    *   KEY_UP: Scroll one line up in the content.

    :return: None.
    :rtype: NoneType

.. class:: thurible.panel.Title(footer_align='left', footer_frame=False \
                                footer_text='', title_align='left', \
                                title_bg='', title_fg='', title_frame=False \
                                title_text='', *args, **kwargs)

    Create a new :class:thurible.panel.Title object. This class serves
    as a parent class for all panels that all the user to put a title
    on the top of the panel and a footer on the bottom of the frame. As
    a subclass of :class:thurible.panel.Frame, it can alse take those
    parameters and has those public methods and properties.
    
    :param footer_align: (Optional.) The horizontal alignment of the
        footer. The available options are "left", "center", and "right".
    :param footer_frame: (Optional.) Whether the frame should be capped
        on either side of the footer.
    :param footer_text: (Optional.) The text contained within the
        footer.
    :param title_align: (Optional.) The horizontal alignment of the
        title. The available options are "left", "center", and "right".
    :param title_bg: (Optional.) The background color of the title and
        footer. See the documentation for :mod:blessed for more detail
        on the available options.
    :param title_fg: (Optional.) The foreground color of the title and
        footer. See the documentation for :mod:blessed for more detail
        on the available options.
    :param title_frame: (Optional.) Whether the frame should be capped
        on either side of the title.
    :param title_text: (Optional.) The text contained within the
        title.
    :return: None.
    :rtype: NoneType

.. property:: Title.footer

    The footer as a string that could be used to update the terminal.
    
    :return: A :class:str object.
    :rtype: str

.. property:: Title.title

    The title as a string that could be used to update the terminal.
    
    :return: A :class:str object.
    :rtype: str

.. _defined:

Defined Panels
**************

The following panels are made available by :mod:thurible to cover common
use cases.

.. class:: thurible.Dialog(message_text, options, *args, **kwargs)

    Create a new :class:thurible.Dialog object. This class displays
    a message to the user and offers pre-defined options for the
    user to chose from. As a subclass of :class:thurible.panel.Content
    and :class:thurible.panel.Title, it can also take those parameters
    and has those public methods and properties.
    
    :param message_text: The text of the prompt to be displayed to
        the user.
    :param options: The options the user can chose from. This is a
        sequence of :class:thurible.Option objects.
    :return: None.
    :rtype: NoneType.
    
.. property:: Dialog.message

    The message as a string that could be used to update the terminal.
    
    :return: A :class:str object.
    :rtype: str
