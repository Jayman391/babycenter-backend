from werkzeug.datastructures import MultiDict

from babycenter_backend.query import QueryWrapper, Loader
from babycenter_backend.topic import TopicWrapper
from babycenter_backend.user import User
from babycenter_backend.runner import Runner

from babycenter_backend.ngram import compute_ngrams

from babycenterdb.post import Post
import json



class RequestHandler:
    def __init__(self):
        self.request_types = ["query", "topic", "ngram", "load", "save"]
        self.users = {}

    def handle(self, request : MultiDict):

        if request["request_type"] not in self.request_types:
            raise ValueError("Invalid request type")
        
        request_type = request["request_type"]

        request.pop("request_type")

        if request['user_id'] is not None:        
            id = request["user_id"]
            if id in self.users:
                user = self.users[id]
        else:
            user = User()
            self.users[user.id] = user

        request.pop("user_id")

        if request_type == "query":
            query = QueryWrapper(**request)
            user.query_data = user.runner.get_data(query)
            return user.query_data
        elif request_type == "save":
            post = Post(request) 
            post.save()
        elif request_type == "load":
            loader = Loader(**request)
            data = Runner().get_precomputed(loader)
            return data
        elif request_type == "ngram":
            if id != 0:
                user = self.users[id]
                user.ngram_data = compute_ngrams(user.query_data, request)
                return user.ngram_data
            else:
                computed_type = 'ngram'
                name = 'full'
                loader = Loader(computed_type=computed_type, name=name)
                data = Runner().get_precomputed(loader)
                return compute_ngrams(data, request)