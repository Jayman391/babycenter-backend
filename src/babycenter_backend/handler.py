from babycenter_backend.query import QueryWrapper
from babycenter_backend.ngram import compute_ngrams
from babycenter_backend.allotax import calculate_divergences

import numpy as np

class RequestHandler:
    def __init__(self):
        self.request_types = ["query", "ngram", "allotax"]
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

            nodate = False

            if request['nodate']:
                nodate = request.pop("nodate", False)
            
            query = QueryWrapper(**request)
            
            query_data = query.execute(nodate)

            self.sessions[sessionID]["queries"].append(query_data)

            return query_data
        elif request_type == "ngram":

            query_data = self.sessions[sessionID]["queries"][-1]

            ngram_data = compute_ngrams(query_data, request)

            self.sessions[sessionID]["ngrams"].append(ngram_data)

            return ngram_data
        
        elif request_type == "allotax":

            groups = request.pop("groups")

            corpora = []

            # build query & ngram requests

            for group in groups:
                # replace _ with space in group str
                postParams = {
                    "request_type": "query",
                    "sessionID": sessionID,
                    "country": "USA",
                    "startDate": "20100101",
                    "endDate": "20240101",
                    "keywords": ['all'],
                    "groups": [group],
                    "num_comments": -1,
                    "post_or_comment": "posts",
                    "num_documents": 2500,
                    "nodate": True
                }

                postData : list = self.handle(postParams)
                
                commentParams = {
                    "request_type": "query",
                    "sessionID": sessionID,
                    "country": "USA",
                    "startDate": "20100101",
                    "endDate": "20240101",
                    "keywords": ['all'],
                    "groups": [group],
                    "num_comments": -1,
                    "post_or_comment": "comments",
                    "num_documents": 2500,
                    "nodate": True
                }

                commentData : list = self.handle(commentParams)
                # join the data

                fetchedData = postData + commentData

                self.sessions[sessionID]["queries"].append(fetchedData)

                ngramParams = {
                    "request_type": "ngram",
                    "sessionID": sessionID,
                    "startDate": "20100101",
                    "endDate": "20240101",
                    "keywords": ['all']
                }

                ngramData = self.handle(ngramParams)['full_corpus']

                ngrams = list(ngramData.keys())
                ranks = [ngramData[ngram]['ranks'] for ngram in ngrams]

                corpora.append(ranks[0])

            divergence_matrix, ngram_index = calculate_divergences(corpora, request.get("alpha"))

             # Serialize for JSON compatibility
            divergence_matrix_serialized = divergence_matrix.tolist()

            ngram_index_serialized = {key: list(value) if isinstance(value, np.ndarray) else value for key, value in ngram_index.items()}

            return {
                "divergence_matrix": divergence_matrix_serialized,
                "ngram_index": ngram_index_serialized
            }

                

                 