import torch
from tools import Tools

""" Train a Neural Network to generate music """
# Get notes from midi files
notes = Tools.get_notes()

# Get the number of pitch names
n_vocab = len(set(notes))

# Convert notes into numerical input
network_input, network_output = Tools.prepare_sequences(notes, n_vocab)
network_input = network_input.tolist()

# Use the model to generate a midi
model = torch.load('lstm_pretrained.pt')
model.eval()
prediction_output = Tools.generate_notes(model, notes,
                                         network_input, len(set(notes)))
Tools.create_midi(prediction_output, 'pokemon_midi_g')