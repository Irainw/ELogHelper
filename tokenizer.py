import re
import os
import requests

class eZTokenizer:
    def __init__(self, vocab):
        self.str2Int = vocab
        self.int2Str = {v: k for k, v in vocab.items()}

    def encode(self, text):
        preprocessed = re.split(r'[,:;?_!"()\']--|\s)', text)
        preprocessed = [item.strip() for item in preprocessed if item.strip()]
        preprocessed = [item if item in self.str2Int else '<unk>' for item in preprocessed]
        
        ids = [self.str2Int[s] for s in preprocessed]
        return ids
    
    def decode(self, ids):
        text = ' '.join([self.int2Str[i] for i in ids])
        text = re.sub(r'\s([,;:.!?])', r'\1', text)
        return text
    