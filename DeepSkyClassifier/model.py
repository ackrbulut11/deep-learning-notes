import torch
import torch.nn as nn

class DeepSkyClassifier(nn.Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.linear_stack_layer = nn.Sequential(
            nn.Linear(6, 16),
            nn.ReLU(),
            nn.Linear(16,16),
            nn.ReLU(),
            nn.Linear(16,6)
        )

    def forward(self, x):
        return self.linear_stack_layer(x)