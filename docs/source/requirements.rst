########################
thurible Requirements
########################

The purpose of this document is to detail the requirements for the
`thurible` package. This is an initial take to help with planning.
There may be additional requirements of non-required features added in
the future that are not recorded here.


Purpose
=======
The purposes of `thurible` are:

*   Create a library of terminal interface widgets.
*   Consolidate terminal interface code I've written.
*   Experiment more with the `blessed` package.


Functional Requirements
=======================
The following are the functional requirements for `thurible`:

*   Provide a program loop in a coroutine that manages:
    *   Output to the terminal,
    *   Input from the keyboard.
*   Display simple log-style output.
*   Display rich text.
*   Display tabular data.
*   Display multipage data.
*   Display command hints.
*   Collect single key presses as input.
*   Collected multicharacter input.
*   Control whether input is echoed to the screen.
*   Split the terminal into sections that can be managed separately.


Technical Requirements
======================
The following are the technical requirements for `thurible`:

*   Be written in Python.
*   Be built on top of the `blessed` package.
*   Have only `blessed` as a third party dependency.
*   Work in:
    *   iTerm2 on macOS,

The following is desired but not initially required:

*   Work in:
    *   Terminal on macOS,
    *   xterm on a Linux platform,
    *   cmd on Windows.


Design Discussion
=================
The following are notes and discussion around the design of `thurible`.
Information here may not reflect the final implementation.


Basic UI Elements
-----------------
The following are the basic UI elements that should be available:

Screen
    The entire display in a terminal. The UI for an application can be
    made of multiple screens.
    
    Note: These are not separate terminal screens like you get with the
    \*nix `screen` command. The `blessed` library cannot create multiple
    of this type of screen. However, it's similar in concept. The 
    application should be able to switch back and forth between multiple
    screens, and the state of those screens should be maintained even
    when they are not being displayed.

Area
    A defined rectangular subsection of a screen. An area is a generic
    type for the defined data views.


Overlap Handling
~~~~~~~~~~~~~~~~
The location and dimensions of an Area seems like it should be a property
of the area. However, an Area should write to the terminal independently
of other Areas. This would mean there is no way for an Area to detect if
it is overlapping with other Areas. If that needs to be detected, it
would need to be done by the Screen.

Does it need to be done? It would avoid needing the application to
handle the need to avoid overlapping Areas. On the other hand, it
would also mean you couldn't choose to overlap areas if you wanted to.
So, maybe, this is something that should be left to the application to
manage.

If overlap is possible, there will need to be a Z axis for the areas to
determine which Area gets to draw in the space. Though for that to work
at the Area level, every change to an Area would necessitate a redraw
of every area. That seems inefficient. So, the Screen will still need to
detect overlaps and determine whether a particular part of an Area is
visible or overlapped. That seems complicated.

Maybe there is a third element needed? It could be a Layer. Areas in a
Layer cannot overlap, but Layers can overlap. That doesn't save us from
having to check what is being overlapped on each draw, though. It just
adds an extra element to the mix that would need to prevent Areas from
overlapping.

Maybe I just do it with proportional frames, like how HTML tables work?
Or, there are different kinds of Screens that manage content differently?
You can have a StaticScreen that sets specific row and column locations
for everything. Then there is a ProportionalScreen that handles frames
like HTML tables. Neither allows overlap.

I may also be overthinking this. Let's not solve this problem at this
time. Let's design everything with fullscreen in mind, but ensure it
can handle the terminal being resized. I can then solve the problem of
having multiple Areas in the same screen after that.


Defined Data Views
------------------
The following are objects that handle displaying common data types
within a UI element.

Blank
    A blank space on the screen.

Text
    Unicode text data that can contain markup for rich text formatting.

Table
    A multidimensional data structure, such as a spreadsheet.

Chart
    A data visualization structure that resembles a bar chart.

Grid
    A data visualization structure that resembles a grid.

Splash
    Ascii art that is usually used to announce that the application
    has launched.


Defined Input Modes
-------------------
The following are objects that can take input from the user.

Keypress
    A single key press from the user.

Field
    A multicharacter string entered by the user and terminated by a return.

Menu
    A selection from a list of options. Navigation through the options
    is done with the arrow keys.

Form
    The collected input from multiple fields. Navigation between fields
    is handled by the return key, the tab key, or the arrow keys.

Prompt
    This is a special type of field that is intended to behave like a
    shell prompt.


Relative Sizing
---------------
The world would be easier if all terminals could only be 80 characters
wide. That is not the case, and so data views need to be able to handle
arbitrary resizing of the terminal both when the application is started
and while it is running. Or, at least, developers need to have the
option to support resizing of the terminal.

To handle this, data views can be given proportional dimensions, such
as 50%. These dimensions are relative to the total dimensions of the
terminal window. They must be recalculated every time a resizing of the
terminal window is detected.


Messaging
---------
The loop for `thurible` should expect to be run in a separate thread
or process. Therefore all interaction with the terminal should be
handled through a queue. There will need to be two queues: an output
queue for messages from the application to the terminal and an input
queue for messages from the terminal to the application. We could make
that more complicated by allowing multiple input and output queues, but
let's keep it simple for now.

Each type of message could be its own class. That would allow specific
behavior to be built into each type of message. I'm not sure that buys
anything over just using a simple data class with two fields: message
and data. I suppose it would allow easier type safety for the data
field. It would lead to there being a lot of different types of messages,
since each data view or input mode will likely need its own series of
messages.


Data Navigation
---------------
Simple navigation of the data, such as scrolling through text and
going to the next form field, should be handled by the Screen rather
than requiring the input to be sent to the application. These are
data views.

This will mean that displays will need to be able to accept input.