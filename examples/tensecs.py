"""
tensecs
~~~~~~~

Show a progress bar indicating the passage of ten seconds.
"""
from threading import Thread
from time import sleep

from thurible import get_queues, queued_manager, Progress
from thurible.progress import Tick
import thurible.messages as tm


# Set up the manager.
q_to, q_from = get_queues()
T = Thread(target=queued_manager, args=(q_to, q_from))
T.start()

# Set up the progress bar.
seconds = 10
interval = 0.125
ticks = int(seconds / interval)
progress = Progress(
    steps=ticks,
    max_messages=4,
    messages=['Waiting…',],
    timestamp=True,
    bar_bg='bright_black',
    frame_type='double',
    title_text='tensecs',
    title_frame=True,
    panel_relative_height=0.3,
    panel_relative_width=0.9,
    content_relative_width=0.9
)

# Display the dialog.
q_to.put(tm.Store('prog', progress))
q_to.put(tm.Show('prog'))

# Putting the loop in a try block to ensure the threads are ended
# if the application runs into a problem.
try:

    # Send an update to the progress bar every eighth of a second for
    # ten seconds.
    for tick in range(ticks):
        sleep(interval)
        msg = f'Waited for {tick * interval:0<2.2f}s.'
        q_to.put(Tick(msg))

except KeyboardInterrupt as ex:
    end = tm.End('Interrupted.')
    q_to.put(end)
    raise ex

# End the program by displaying the favorite word.
end = tm.End('That was at least 10 seconds.')
q_to.put(end)
