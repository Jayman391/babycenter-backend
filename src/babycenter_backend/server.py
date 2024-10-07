from flask import Flask, request, jsonify
import paramiko
from flask_cors import CORS
from babycenter_backend.handler import RequestHandler

handler = RequestHandler()
query_factory = handler.query_factory
topic_factory = handler.topic_factory
user_factory = handler.user_factory

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes and origins

# Refactored /query route to use request.args instead of URL parameters
@app.route('/query', methods=['GET'])
def query():
    try:
        # Extract query parameters from request.args
        country = request.args.get('country')
        format = request.args.get('format')
        start = request.args.get('start')
        end = request.args.get('end')
        keywords = request.args.get('keywords', '').split(',')
        groups = request.args.get('groups', '').split(',')
        num_comments = request.args.get('num_comments', type=int)
        post_or_comment = request.args.get('post_or_comment')
        num_documents = request.args.get('num_documents', type=int)

        # create user
        user = user_factory.create_user()
        user.query_created = True
        handler.users[user.id] = user

        # Construct params for handler
        params = {
            "request_type": "query",
            "user_id": user.id,
            "country": country,
            "format": format,
            "start": start,
            "end": end,
            "keywords": keywords,
            "groups": groups,
            "num_comments": num_comments,
            "post_or_comment": post_or_comment,
            "num_documents": num_documents
        }

        response = handler.handle(params)
        return jsonify({"user": user.id, "response": response})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


# Refactored /topic route to use request.args
@app.route('/topic', methods=['GET'])
def topic():
    try:
        # Extract query parameters from request.args
        user_id = request.args.get('user_id')
        embedding = request.args.get('embedding')
        dimred = request.args.get('dimred')
        clustering = request.args.get('clustering')
        vectorizer = request.args.get('vectorizer')

        return jsonify({
            "status": "success",
            "message": "Topic modeling successful",
            "content": {
                "embedding": embedding,
                "dimred": dimred,
                "clustering": clustering,
                "vectorizer": vectorizer,
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


# Refactored /ngram route to use request.args
@app.route('/ngram', methods=['GET'])
def ngram():
    try:
        # Extract query parameters from request.args
        user_id = request.args.get('user_id')
        country = request.args.get('country')
        start = request.args.get('start')
        end = request.args.get('end')
        keywords = request.args.get('keywords', '').split(',')

        return jsonify({
            "status": "success",
            "message": "Visualization successful",
            "content": {
                "country": country,
                "start": start,
                "end": end,
                "keywords": keywords
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


"""
@app.route("/auth/<username>/<password>", methods=['GET'])
def auth(username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect('vacc-user1.uvm.edu', username=username, password=password)
        return jsonify({"status": "success", "message": "Authentication successful"})
    except Exception as e:
        return jsonify({"status": "error", "message": e})
"""

if __name__ == '__main__':
    app.run(debug=True)
