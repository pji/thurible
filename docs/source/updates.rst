.. _updates:

############
Update Notes
############
The following are the notes on updates to :mod:`thurible`.


.. _v0_0_2:

Changes in 0.0.2
****************
The following are the changes in v0.0.2:

*   Moved dependency management to `poetry`.
*   Moved `thurible` into a `src` folder.
*   Moved testing to `pytest`.
*   Fixed unsafe terminal behavior in `thurible.thurible` tests.
*   Implemented `tox` to test across supported Python versions.
*   Moved doctests to `sphinx`.
*   Handled exceptions that may raise when changing terminal size in
    :func:`thurible.queued_manager`.
*   Added `py.typed` file.
*   Fixed typing issues from `examples`.
*   Documentation formatting changes.


.. _todo:

To-Do List
**********
The following items are likely in future releases:

*   Manager updates:

    *   Add coroutine manager.
    
*   Panel updates:

    *   Fall back frames that only use ASCII characters.
    *   Fall back overflow indicators that only use ASCII characters.
    *   Simplify sizing.
    *   Add a simple table for sequences.
    *   Add a simple table for mappings.
    *   Add a textfield panel.
    *   Add a textform panel.
    *   Add a tableform panel.
    *   Figure out what to do if dialog message overflows.
