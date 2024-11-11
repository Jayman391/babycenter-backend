import unittest
import os
import sys

# Ensure the correct path to access the backend source code.
# might have to run this : export PYTHONPATH=$PYTHONPATH:/Users/user/Desktop/babycenter-backend/src
sys.path.append(os.path.abspath("../src"))

from babycenter_backend.handler import RequestHandler

from uuid import uuid4


class TestHandler(unittest.TestCase):

    def setUp(self):
        self.handler = RequestHandler()

    def test_handle_query_no_user(self):
        request = {
            "request_type": "query",
            "country": "USA",
            "startDate": "20200101",
            "endDate": "20200131",
            "keywords": ["baby"],
            "groups": ["all"],
            "num_comments": 10,
            "post_or_comment": "posts",
            "num_documents": 10,
        }
        response = self.handler.handle(request)
        self.assertTrue(len(self.handler.users.keys()) > 0)
        self.handler.users = {}
        self.assertTrue(type(response) == list)

    def test_ngram(self):
        id = uuid4().hex
        query_request = {
            "request_type": "query",
            "user_id": id,
            "country": "USA",
            "startDate": "20200101",
            "endDate": "20200131",
            "keywords": ["baby"],
            "groups": ["all"],
            "num_comments": 10,
            "post_or_comment": "posts",
            "num_documents": 10,
        }

        self.handler.handle(query_request)

        ngram_request = {
            "request_type": "ngram",
            "user_id": id,
            "startDate": "20200101",
            "endDate": "20200131",
            "keywords": ["all"],
        }

        response = self.handler.handle(ngram_request)
        self.assertTrue(response)
        self.assertIsInstance(response, dict)

    def test_save(self):
        request = {
            "request_type": "save",
            "_id": "testsave" + uuid4().hex,
            "type": "test",
            "content": {"test": "test"},
        }
        response = self.handler.handle(request)
        self.assertEqual(response, {"status": "success"})

    def test_load(self):
        id = uuid4().hex
        post_request = {
            "request_type": "save",
            "id": "testsave" + id,
            "type": "query",
            "content": {"test": "test"},
        }
        self.handler.handle(post_request)

        get_request = {
            "request_type": "load",
            "type": "query",
            "user_id": "testsave",
        }
        response = self.handler.handle(get_request)
        # assert response is not empty and is a dictionary
        self.assertTrue(response)
        self.assertIsInstance(response[0], dict)

