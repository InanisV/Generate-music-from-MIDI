import sys
import torch
from tools import Tools

""" Generate the music from a random midi in training set"""
# Get notes from midi files
dataset_name = sys.argv[1]
notes = Tools.load_obj(f'{dataset_name}_notes')

# Get the number of pitch names
n_vocab = len(set(notes))

# Convert notes into numerical input
network_input, network_output = Tools.prepare_sequences(notes, n_vocab)
network_input = network_input.tolist()

# Use the model to generate a midi
model = torch.load(f'lstm_pretrained_{dataset_name}.pt')
model.eval()
prediction_output = Tools.generate_notes(model, notes,
                                         network_input, len(set(notes)))
Tools.create_midi(prediction_output, f'{dataset_name}_midi_g')
