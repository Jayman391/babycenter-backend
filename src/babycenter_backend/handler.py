from babycenter_backend.query import QueryWrapper
from babycenter_backend.ngram import compute_ngrams

class RequestHandler:
    def __init__(self):
        self.request_types = ["query", "ngram"]
        self.sessions = {}

    def handle(self, request):
        if request["request_type"] not in self.request_types:
            raise ValueError("Invalid request type")

        request_type = request.pop("request_type")
        sessionID = request.pop("sessionID")

        if not self.sessions.get(sessionID):
           self.sessions[sessionID] = {
               "queries" : [],
               "ngrams" : []
           }
      
        if request_type == "query":
            query = QueryWrapper(**request)
            query_data = query.execute()

            self.sessions[sessionID]["queries"].append(query_data)

            return query_data
        elif request_type == "ngram":

            query_data = self.sessions[sessionID]["queries"][-1]

            ngram_data = compute_ngrams(query_data, request)

            self.sessions[sessionID]["ngrams"].append(ngram_data)

            return ngram_data
