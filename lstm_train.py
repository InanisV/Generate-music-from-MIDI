import torch
from torch import nn, optim
from tools import Tools
from lstm_model import MyLSTM


# CUDA for PyTorch
use_cuda = torch.cuda.is_available()
device = torch.device("cuda:0" if use_cuda else "cpu")

""" Train a Neural Network to generate music """
# Get notes from midi files
notes = Tools.get_notes()

# Get the number of pitch names
n_vocab = len(set(notes))

# Convert notes into numerical input
network_input, network_output = Tools.prepare_sequences(notes, n_vocab)
print(type(network_input))
network_input = network_input.tolist()
network_output = network_output.tolist()
# my_input = torch.from_numpy(network_input)
my_input = torch.DoubleTensor(network_input)
# print(my_input)
my_output = torch.DoubleTensor(network_output)
dataset = torch.utils.data.TensorDataset(my_input, my_output)
loader = torch.utils.data.DataLoader(dataset, batch_size=512, shuffle=True)

# Set up the model
print(list(my_input.size()))
model = MyLSTM(n_vocab)
model = model.double()
model.to(device)
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters())
# history = History()

# Fit the model
for epoch in range(10):
    running_loss = 0.
    running_mae = 0.

    for i, data in enumerate(loader):
        inputs, labels = data
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        print(type(inputs))
        # print(inputs)
        outputs = model(inputs)
        print(list(outputs.size()))
        print(list(labels.size()))
        # outputs = outputs[-1].view(*labels.shape)
        l, n, m = outputs.shape
        outputs = torch.reshape(outputs, (n, m))
        # print(labels[0])
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        # mae = mean_absolute_error(labels.detach().cpu().numpy().flatten(),
        # outputs.detach().cpu().numpy().flatten())
        # running_mae += mae

    print('EPOCH %3d: loss %.5f' % (epoch+1, running_loss/len(loader)))
    torch.save(model, 'lstm_pretrained.pt')

# Use the model to generate a midi
model = torch.load('lstm_pretrained.pt')
model.eval()
prediction_output = Tools.generate_notes(model, notes,
                                         network_input, len(set(notes)))
Tools.create_midi(prediction_output, 'pokemon_midi')
