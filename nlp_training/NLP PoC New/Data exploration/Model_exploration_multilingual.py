import pandas as pd
import numpy as np
import os
import gc

import random

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

# set a seed value
torch.manual_seed(555)

from sklearn.utils import shuffle
from sklearn.metrics import roc_auc_score, accuracy_score

import transformers
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import XLMRobertaTokenizer, XLMRobertaForSequenceClassification
from transformers import AdamW

# import torch_xla
# import torch_xla.core.xla_model as xm

import warnings
warnings.filterwarnings("ignore")


print(torch.__version__)

MODEL_TYPE = 'xlm-roberta-base'


L_RATE = 1e-5
MAX_LEN = 256

NUM_EPOCHS = 3
BATCH_SIZE = 32
NUM_CORES = os.cpu_count()

print(NUM_CORES)

