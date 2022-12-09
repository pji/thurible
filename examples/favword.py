"""
favword
~~~~~~~

Prompt the user for their favorite word, then repeat the word to them.
"""
from threading import Thread

from thurible import get_queues, queued_manager, TextDialog
import thurible.messages as tm


# Set up the manager.
q_to, q_from = get_queues()
T = Thread(target=queued_manager, args=(q_to, q_from))
T.start()

# Set up dialog.
dialog = TextDialog(
    message_text='What is your favorite word?',
    title_text='Favorite Word',
    frame_type='heavy'
)

# Display the dialog.
q_to.put(tm.Store('dialog', dialog))
q_to.put(tm.Show('dialog'))

# Poll the manager until we get the answer to the question.
msg = None
while not isinstance(msg, tm.Data):
    if not q_from.empty():
        msg = q_from.get()
fav_word = msg.value

# End the program by displaying the favorite word.
end = tm.End(f'Your favorite word is {fav_word}.')
q_to.put(end)
