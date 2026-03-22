import torch
import torch.nn as nn


class IrisClassifier(nn.Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.linear_layer_stack = nn.Sequential(
            nn.Linear(4, 12),
            nn.ReLU(),

            nn.Linear(12, 12),
            nn.ReLU(),

            nn.Linear(12, 3)
        )

    def forward(self, x):
        return self.linear_layer_stack(x)
