from babycenter_backend.query import QueryWrapper, Loader
from babycenter_backend.user import User
from babycenter_backend.runner import Runner
from babycenter_backend.ngram import compute_ngrams
from babycenterdb.post import Post

class RequestHandler:
    def __init__(self):
        self.request_types = ["query", "topic", "ngram", "load", "save"]
        self.users = {}

    def handle(self, request):
        if request["request_type"] not in self.request_types:
            raise ValueError("Invalid request type")

        request_type = request.pop("request_type")
        user_id = request.pop("user_id", None)

        if user_id:
            # User ID corresponds to username
            if user_id in self.users:
                user = self.users[user_id]
            else:
                user = User(username=user_id)
                self.users[user_id] = user
        else:
            user = User()
            user_id = user.id
        
        if request_type == "query":
            query = QueryWrapper(**request)
            user.query_data = user.runner.get_data(query)
            return user.query_data
        elif request_type == "save":
            post = Post(request)
            post.save()
            return {"status": "success"} 
        elif request_type == "load":
            request['name'] = user_id
            loader = Loader(**request)
            data = user.runner.get_precomputed(loader)
            return data
        elif request_type == "ngram":
            user.ngram_data = compute_ngrams(user.query_data, request)
            return user.ngram_data
