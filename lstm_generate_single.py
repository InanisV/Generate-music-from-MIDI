import pickle
import torch
from tools import Tools


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


""" Generate the music from a single midi """
# Get notes from midi file
# The directory only contains that one midi (simply to reuse the code)
notes = Tools.get_notes("generate src/*.mid")

# Get the number of pitch names
n_vocab = len(set(notes))

note_to_int = load_obj('note2int')
int_to_note = load_obj('int2note')

# Convert notes into numerical input
network_input = Tools.prepare_sequences_single(notes, note_to_int, n_vocab)
network_input = network_input.tolist()

# Use the model to generate a midi
model = torch.load('lstm_pretrained.pt')
model.eval()
prediction_output = Tools.generate_notes_single(model, int_to_note,
                                                network_input, len(set(notes)))
Tools.create_midi(prediction_output, 'pokemon_midi_g')
