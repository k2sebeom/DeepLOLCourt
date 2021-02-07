import torch.nn as nn


class LOLResultModel(nn.Module):
    def __init__(self, in_feature):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(in_feature, 128),
            nn.BatchNorm1d(128),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.BatchNorm1d(32),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.layers(x)
