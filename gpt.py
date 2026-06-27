import torch
import torch.nn as nn
from torch.nn import functional as F

batchSize = 64
blockSize = 256
maxIters = 5000
evalInterval = 500
learningRate = 3e-4
device = 'cuda' if torch.cuda.is_available() else 'cpu'
evalIters = 200
nEmbed = 384
nHead = 6
nLayer = 6
dropout = 0.2

torch.manual_seed(531434)

# Next steps:
# 1. Generate text file from the ELog and Wiki data and save it as 'input.txt'.
# 2. Create a character vocabulary and map the characters to integers.
# 3. Encode the text into integers and split it into training and validation sets.