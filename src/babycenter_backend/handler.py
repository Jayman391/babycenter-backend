from werkzeug.datastructures import MultiDict

from babycenter_backend.query import QueryWrapper
from babycenter_backend.topic import TopicWrapper
from babycenter_backend.user import User


class RequestHandler:
    def __init__(self):
        self.request_types = ["query", "topic", "ngram", "precomputed"]
        self.users = {}

    def handle(self, request : MultiDict):
        if request["request_type"] not in self.request_types:
            raise ValueError("Invalid request type")
        
        request_type = request["request_type"]

        request.pop("request_type")

        user = self.users[request["user_id"]]

        request.pop("user_id")

        if request_type == "query":
            query = QueryWrapper(request)
            user.query_data = user.runner.get_data(query)
            return user.query_data