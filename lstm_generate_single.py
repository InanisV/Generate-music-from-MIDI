import sys
import torch
from tools import Tools

""" Generate the music from a single midi """
# Get notes from midi file
# The directory only contains that one midi (simply to reuse the code)
dataset_name = sys.argv[1]
notes = Tools.get_notes("generate src/*.mid")

# Get the number of pitch names
n_vocab = len(set(notes))

note_to_int = Tools.load_obj(f'{dataset_name}_note2int')
int_to_note = Tools.load_obj(f'{dataset_name}_int2note')

# Convert notes into numerical input
network_input = Tools.prepare_sequences_single(notes, note_to_int, n_vocab)
network_input = network_input.tolist()

# Use the model to generate a midi
model = torch.load(f'lstm_pretrained_{dataset_name}.pt')
model.eval()
prediction_output = Tools.generate_notes_single(model, int_to_note,
                                                network_input, len(set(notes)))
Tools.create_midi(prediction_output, f'{dataset_name}_midi_g')
