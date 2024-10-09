from babycenter_backend.query import QueryWrapper
from babycenter_backend.topic import TopicWrapper
from babycenter_backend.ngram import compute_ngrams
from typing import Dict, List 

class Runner:
  def __init__(self) -> None:
    pass
  def get_data(self, query : QueryWrapper) -> List[Dict]:
    return query.execute() 
  def run_topic_model(self, topic : TopicWrapper) -> Dict[str, Dict[str, str]]:
    pass
  def compute_ngrams(self, content : Dict) -> Dict[str, List[int]]:
    pass
  def get_precomputed(self, content : Dict) -> Dict[str, Dict[str, str]]:
    pass

