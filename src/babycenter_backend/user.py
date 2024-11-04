from babycenter_backend.runner import Runner
from uuid import uuid4

class User:
    def __init__(self, username = uuid4()): 
        self.id = username  # Set the user ID to the username
        self.runner = Runner()
        self.query_created = False
        self.query_data = {}
        self.ngram_data = {}