import torch
import torch.nn as nn
import sys
    

class Net_1(nn.Module):
    def __init__(self, input):
        super().__init__()
        self.input_layer = nn.Linear(input, 128)
        self.hidden_layer = nn.Linear(128, 64)
        self.output_layer = nn.Linear(64, 1)
        self.act = nn.ELU()

    def forward(self, x):
        x = self.act(self.input_layer(x))
        x = self.act(self.hidden_layer(x))
        y = self.output_layer(x)
        return y
    
class Net_embedding(nn.Module):
    def __init__(self, vocab_size, embedding_dim=None):
        super().__init__()
        if embedding_dim is None:
            embedding_dim = [ 8 for _ in vocab_size]
        input = sum(embedding_dim) + 3
        self.input_layer = nn.Linear(input, 128)
        self.hidden_layer = nn.Linear(128, 64)
        self.output_layer = nn.Linear(64, 1)
        self.act = nn.ReLU()
        self.embedding_layers = nn.ModuleList([
            nn.Embedding(num_vocab+1, embedding_dim) for num_vocab, embedding_dim in zip(vocab_size, embedding_dim)
        ])

    def forward(self, x, z):
        embedded_features = [embedding(x[:, i]) for i, embedding in enumerate(self.embedding_layers)]
        flattened_features = torch.cat(embedded_features, dim=1)
        x = torch.cat([flattened_features, z], dim=1)

        x = self.act(self.input_layer(x))
        x = self.act(self.hidden_layer(x))
        y = self.output_layer(x)
        return y
