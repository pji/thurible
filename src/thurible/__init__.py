"""
__init__
~~~~~~~~

Initialization for the `thurible` package.
"""
import sys as _sys


# Subscripting of type is not supported before Python 3.9.
if _sys.version_info[:2] < (3, 9):
    msg = 'Thurible requires Python 3.9 or higher.'
    raise ImportError(msg)

from blessed import Terminal
from blessed.keyboard import Keystroke

from thurible.dialog import Dialog
from thurible.eventmanager import event_manager
from thurible.log import Log, Update
from thurible.menu import Menu, Option
from thurible.progress import NoTick, Progress, Tick
from thurible.splash import Splash
from thurible.table import Table
from thurible.text import Text
from thurible.textdialog import TextDialog
from thurible.thurible import queued_manager
from thurible.util import get_queues, get_terminal
