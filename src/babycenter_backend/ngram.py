from datetime import datetime
from collections import Counter
import re
import numpy as np

def compute_ngrams(data: list, params: dict) -> dict:
    dates = {}

    ngrams = params["keywords"]
    ns = [1]
    for ngram in ngrams:
        length = len(ngram.split())
        if length > 1:
            ns.append(length)
    if "all" in ngrams:
        ngrams.remove("all")
        if not ngrams:
            ngrams = []
    ns = np.unique(ns)

    for doc in data:
        # Ensure date is a datetime object
        if isinstance(doc["date"], str):
            date_obj = datetime.strptime(doc["date"], '%Y-%m-%d')
        else:
            date_obj = doc["date"]
        date_str = date_obj.strftime('%a, %d %b %Y %H:%M:%S')

        if date_str not in dates:
            dates[date_str] = {}
            for n in ns:
                dates[date_str][f'{n}-gram'] = Counter()

        # Combine 'text' and 'title' if 'title' exists
        text = doc["text"]
        if 'title' in doc and doc['title']:
            text += ' ' + doc['title']
        text = text.lower()

        # Remove special characters
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

        for n in ns:
            chunks = chunk_text(text, n)
            for chunk in chunks:
                if ngrams and chunk in ngrams:
                    dates[date_str][f'{n}-gram'][chunk] += 1
                elif not ngrams:
                    dates[date_str][f'{n}-gram'][chunk] += 1

    return dates

def chunk_text(text: str, n: int = 1):
    words = text.split()
    return [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]
