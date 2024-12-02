import torch
import torch.nn as nn

class BiscuitPlacementNN(nn.Module):
    def __init__(self, input_size=20, hidden_size=64, output_size=4):
        super(BiscuitPlacementNN, self).__init__()
        
        # Adjust input_size if necessary
        self.fc1 = nn.Linear(input_size, hidden_size)  # input_size should be 4 if you're using one-hot encoding with 4 categories
        #self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        #x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x