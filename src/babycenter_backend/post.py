from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import pandas as pd
 
class Post:
    CONNECTION_STRING = "mongodb://cwward:password@wranglerdb01a.uvm.edu/?authMechanism=DEFAULT"
    DATABASE_NAME = "babynamesDB"
    def __init__(self, content: dict) -> None:
        self.client = MongoClient(self.CONNECTION_STRING)
        try:
            self.client.server_info()
        except ServerSelectionTimeoutError as e:
            raise Exception(f"There was an issue when trying to connect the BabyCenter DB. Make sure that you are connected the UVM VPN. FULL STACKTRACE: {e}")
        self.db = self.client[f"{self.DATABASE_NAME}"]
        self.collection = self.db["precomputed"]
        self.content = content
 
    def save(self):
        try:
            self.collection.insert_one(self.content)
        except Exception as e:
            raise Exception(f"There was an issue when trying to insert the content into the collection. FULL STACKTRACE: {e}")