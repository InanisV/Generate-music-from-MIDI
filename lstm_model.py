import torch
import torch.nn as nn


class MyLSTM(nn.Module):
    def __init__(self, n_vocab):
        super(MyLSTM, self).__init__()

        # Sequential layers
        self.lstm1 = nn.LSTM(input_size=100, hidden_size=512,
                             dropout=0.3, batch_first=True)
        self.lstm2 = nn.LSTM(input_size=512, hidden_size=512, dropout=0.3,
                             bidirectional=True, batch_first=True)
        self.lstm3 = nn.LSTM(input_size=1024, hidden_size=512,
                             bidirectional=True, batch_first=True)
        self.dense1 = nn.Linear(1024, 256)
        self.dropout = nn.Dropout(0.3)
        self.dense2 = nn.Linear(256, n_vocab)
        self.softmax = nn.Softmax()

    def forward(self, x):

        # Sequential layers
        # print(type(x))
        # print(list(x.size()))
        x = x.permute([2,0,1])
        x, _ = self.lstm1(x)
        # print(list(x.size()))
        x, _ = self.lstm2(x)
        # print(list(x.size()))
        x, _ = self.lstm3(x)
        # print(list(x.size()))
        x = self.dense1(x)
        # print(list(x.size()))
        x = self.dropout(x)
        x = self.dense2(x)
        # print(list(x.size()))
        x = self.softmax(x)

        return x
