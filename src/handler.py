from flask import Request, Response
from src.query import Query, QueryFactory
from src.topic import Topic, TopicFactory
from src.user import User

class RequestHandler:
    def __init__(self):
        self.request_types = ["query", "topic", "ngram", "precomputed"]
        self.users = {}
        self.query_factory = QueryFactory()
        self.topic_factory = TopicFactory()
    def handle(self, request : Request) -> Response:
        pass
    def create_user(self):
        pass
    def remove_user(self, user_id):
        pass