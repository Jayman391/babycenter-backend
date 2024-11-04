from babycenter_backend.query import QueryWrapper, Loader
from babycenter_backend.ngram import compute_ngrams
from typing import Dict, List 

class Runner:
  def __init__(self) -> None:
    pass
  def get_data(self, query : QueryWrapper) -> List[Dict]:
    return query.execute() 
  def compute_ngrams(self, data : List, content : Dict) -> Dict[str, List[int]]:
    return compute_ngrams(data, content)
  def get_precomputed(self, loader : Loader) -> Dict[str, Dict[str, str]]:
    return loader.execute()

