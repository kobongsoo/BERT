import os
import random
import numpy as np
import torch
import time

from tqdm.notebook import tqdm
from torch.utils.data.dataset import Dataset
#=====================================================================================
# gpt2-text generation dataset 생성 
#
# => 입력 : 문장들.
# => 출력 : input_ids => bos_token + 문장 + eos_token
#           attention_maskes => 111111000000
#=====================================================================================
def TextGeneration_tokenizer_seq(sentence, tokenizer, max_length):
    return tokenizer(tokenizer.bos_token + sentence + tokenizer.eos_token, truncation=True, max_length=max_length, padding="max_length")

class TextGeneration_Dataset(Dataset):
    def __init__(self, sentences, tokenizer, gpt2_type="gpt2", max_length=128):
        
        self.tokenizer = tokenizer
        self.input_ids = []
        self.attention_masks = []
        
        for sentence in tqdm(sentences):
            encodings = TextGeneration_tokenizer_seq(sentence, tokenizer, max_length)
            #print(encodings) break
            self.input_ids.append(torch.tensor(encodings['input_ids']))
            self.attention_masks.append(torch.tensor(encodings['attention_mask']))
            
    def __len__(self):
        return len(self.input_ids)
    
    def __getitem__(self, idx):
        return self.input_ids[idx], self.attention_masks[idx]
#=====================================================================================