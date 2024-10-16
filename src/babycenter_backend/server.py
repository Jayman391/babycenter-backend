from flask import Flask, request, jsonify
from flask_cors import CORS
from babycenter_backend.handler import RequestHandler
from babycenter_backend.user import User

handler = RequestHandler()

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes and origins

# Refactored /query route to use request.args instead of URL parameters
@app.route('/query', methods=['GET'])
def query():
    try:
        # Extract query parameters from request.args
        country = request.args.get('country')
        start = request.args.get('startDate')
        end = request.args.get('endDate')
        keywords = request.args.get('keywords', '').split(',')
        groups = request.args.get('groups', '').split(',')
        num_comments = request.args.get('num_comments', type=int)
        post_or_comment = request.args.get('post_or_comment')
        num_documents = request.args.get('num_documents', type=int)
        # create user
        user = User()
        user.query_created = True
        handler.users[user.id] = user

        # Construct params for handler
        params = {
            "request_type": "query",
            "user_id": user.id,
            "country": country,
            "startDate": start,
            "endDate": end,
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

@app.route('/save', methods=['POST'])
def save():
    try:
        user_id = 0
        type = request.json.get('type')
        name = request.json.get('name')
        content = request.json.get('content')

        params = {
            "request_type": "save",
            "user_id": user_id,
            "type": type,
            "_id": name,
            "content": content
        }

        handler.handle(params)

        return jsonify({"status": "success", "message": "Data saved successfully"})
    
    except Exception as e:

        return jsonify({"status": "error", "message": str(e)})
    
@app.route('/load', methods=['GET'])
def load():
    try:
        user_id = 0
        computed_type = request.args.get('computed_type')
        name = request.args.get('name')
        all = request.args.get('all')

        params = {
            "request_type": "load",
            "user_id": user_id,
            "computed_type": computed_type,
            "name": name,
            "all": all
        }

        response = handler.handle(params)
        return jsonify({"status": "success", "message": "Data loaded successfully", "content": response})

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
