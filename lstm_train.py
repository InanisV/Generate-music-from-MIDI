import csv
import torch
from torch import nn, optim
from tools import Tools
from lstm_model import MyLSTM
from tqdm import tqdm
from torch.optim.lr_scheduler import StepLR


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
network_input = network_input.tolist()
network_output = network_output.tolist()

my_input = torch.DoubleTensor(network_input)
my_output = torch.DoubleTensor(network_output)
dataset = torch.utils.data.TensorDataset(my_input, my_output)
loader = torch.utils.data.DataLoader(dataset, batch_size=512, shuffle=True)

# Set up the model
model = MyLSTM(n_vocab)
model = model.double()
model.to(device)
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.003)
scheduler = StepLR(optimizer, step_size=1, gamma=0.98)

# Fit the model
with open('Training_log.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Epoch', 'BCELoss', 'LearningRate'])
    for epoch in range(200):
        running_loss = 0.

        with tqdm(loader, unit="batch") as tepoch:
            tepoch.set_description(f"Epoch {epoch+1}")
            for data in tepoch:
                inputs, labels = data
                inputs, labels = inputs.to(device), labels.to(device)
                optimizer.zero_grad()
                outputs = model(inputs)
                l, n, m = outputs.shape
                outputs = torch.reshape(outputs, (n, m))
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                running_loss += loss.item()
                tepoch.set_postfix(loss=loss.item())

        avg_loss = running_loss/len(loader)
        lr = optimizer.param_groups[0]['lr']
        print('EPOCH %3d: loss %.5f' % (epoch+1, avg_loss))
        writer.writerow([(epoch+1), round(avg_loss, 5), round(lr, 5)])
        scheduler.step()
        # torch.save(model, 'lstm_pretrained.pt')

model_cpu = model.cpu()
torch.save(model, 'lstm_pretrained.pt')
print('Finish training :)')

# Use the model to generate a midi
model = torch.load('lstm_pretrained.pt')
model.eval()
prediction_output = Tools.generate_notes(model, notes,
                                         network_input, len(set(notes)))
Tools.create_midi(prediction_output, 'pokemon_midi')
print('Finish generating :D')
