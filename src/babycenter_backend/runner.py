from query import Query
from topic import Topic
from ngram import compute_ngrams
from typing import Dict, List 

class Runner:
  def __init__(self) -> None:
    pass
  def get_data(self, query : Query) -> Dict[str, Dict[str, str]]:
    pass
  def run_topic_model(self, topic : Topic) -> Dict[str, Dict[str, str]]:
    pass
  def compute_ngrams(self, content : Dict) -> Dict[str, List[int]]:
    pass
  def get_precomputed(self, content : Dict) -> Dict[str, Dict[str, str]]:
    pass

