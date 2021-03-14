import pickle
from tools import Tools


def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


""" Build and save note dictionarys """
# Get notes from midi files
notes = Tools.get_notes("Pokemon MIDIs/*.mid")

# Get the number of pitch names
n_vocab = len(set(notes))

# Convert notes into numerical input
note_to_int, int_to_note = Tools.get_note_dicts(notes)

save_obj(note_to_int, 'note2int')
save_obj(int_to_note, 'int2note')
