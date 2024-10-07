from runner import Runner
from uuid import uuid4

class User:
    def __init__(self): 
        self.id = uuid4() 
        self.runner = Runner()
        self.query_created = False
        self.query_data = {}
        self.topic_data = {}
        self.ngram_data = {}