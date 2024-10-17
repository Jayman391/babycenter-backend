from datetime import datetime
from collections import Counter
import re 
import numpy as np

def compute_ngrams(data : dict, params : dict) -> dict:

    dates = {}

    ngrams = params["keywords"]
    ns = [1]
    for ngram in ngrams:
        length = len(ngram.split())
        if length > 1:
            ns.append(length)
        if ngram == "all":
            # remove all from ngrams list
            ngrams = set(ngrams).remove("all")
            if ngrams is None:
                ngrams = []
    
    ns = np.unique(ns)
    
    for doc in data:
        date = doc["date"].strftime('%a, %d %b %Y %H:%M:%S')

        if dates.get(date) is None:
            dates[date] = {}
            for n in ns:
                dates[date][f'{n}-gram'] = Counter()

        text = doc["text"] + doc["title"]
        text = text.lower()

        # Remove special characters
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

        for n in ns:
            chunks = chunk_text(text, n)
            for chunk in chunks:
                if len(ngrams) != 0 and chunk in ngrams:
                    dates[date][f'{n}-gram'][chunk] += 1
                elif len(ngrams) == 0:
                    dates[date][f'{n}-gram'][chunk] += 1

    return dates
            
def chunk_text(text : str, n : int = 1):
    text = text.split()
    return ["".join(text[i:i+n]) for i in range(len(text)-n+1)]