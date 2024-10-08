from werkzeug.datastructures import MultiDict

from babycenter_backend.query import QueryFactory
from babycenter_backend.topic import TopicFactory
from babycenter_backend.user import UserFactory


class RequestHandler:
    def __init__(self):
        self.request_types = ["query", "topic", "ngram", "precomputed"]
        self.users = {}
        self.query_factory = QueryFactory()
        self.topic_factory = TopicFactory()
        self.user_factory = UserFactory()

    def handle(self, request : MultiDict):
        if request["request_type"] not in self.request_types:
            raise ValueError("Invalid request type")
        
        request_type = request["request_type"]

        request.pop("request_type")

        user = self.users[request["user_id"]]

        request.pop("user_id")

        if request_type == "query":
            query = self.query_factory.create_query(request)
            user.query_data = user.runner.get_data(query)
            return user.query_data