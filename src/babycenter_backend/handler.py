from flask import Request, Response
from query import Query, QueryFactory
from topic import Topic, TopicFactory
from user import User, UserFactory

class RequestHandler:
    def __init__(self):
        self.request_types = ["query", "topic", "ngram", "precomputed"]
        self.users = {}
        self.query_factory = QueryFactory()
        self.topic_factory = TopicFactory()
        self.user_factory = UserFactory()
        
    def handle(self, request : Request) -> Response:
        pass
   