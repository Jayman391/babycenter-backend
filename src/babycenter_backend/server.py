from flask import Flask, request, jsonify
from flask_cors import CORS
from babycenter_backend.handler import RequestHandler
from babycenter_backend.user import User

handler = RequestHandler()

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes and origins

@app.route('/query', methods=['GET'])
def query():
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            raise ValueError("User ID is required.")
        # Extract query parameters from request.args
        country = request.args.get('country')
        start = request.args.get('startDate')
        end = request.args.get('endDate')
        keywords = request.args.get('keywords', '').split(',')
        groups = request.args.get('groups', '').split(',')
        num_comments = request.args.get('num_comments', type=int)
        post_or_comment = request.args.get('post_or_comment')
        num_documents = request.args.get('num_documents', type=int)


        # Create or retrieve user
        if user_id in handler.users:
            user = handler.users[user_id]
        else:
            user = User(username=user_id)
            handler.users[user_id] = user
        user.query_created = True

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
        data = request.json
        user_id = data.get('content', {}).get('userId')  # Extract userId from content
        post_id = data.get('_id')  # Extract the unique _id field

        if not post_id or not user_id:
            raise ValueError("Invalid save request: Missing _id or userId.")

        # Handle the save logic using the provided _id and content
        params = {
            "request_type": "save",
            "user_id": user_id,
            "_id": post_id,
            "type": data.get('type'),
            "content": data.get('content'),
        }

        handler.handle(params)

        return jsonify({"status": "success", "message": "Data saved successfully"})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

    
@app.route('/load', methods=['GET'])
def load():
    try:
        user_id = request.args.get('user_id', None)
        computed_type = request.args.get('computed_type')
        name = request.args.get('name')

        params = {
            "request_type": "load",
            "user_id": user_id,
            "computed_type": computed_type,
            "name": name,
        }

        response = handler.handle(params)
        return jsonify({"status": "success", "message": "Data loaded successfully", "content": response})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/ngram', methods=['GET'])
def ngram():
    try:
        # Extract query parameters from request.args
        user_id = request.args.get('user_id')
        if not user_id:
            raise ValueError("User ID is required.")
        start = request.args.get('startDate')
        end = request.args.get('endDate')
        keywords = request.args.get('keywords', '').split(',')

        params = {
            "request_type": "ngram",
            "user_id": user_id,
            "startDate": start,
            "endDate": end,
            "keywords": keywords
        }

        response = handler.handle(params)

        return jsonify({"status": "success", "message": "Ngram computation successful", "content": response})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
