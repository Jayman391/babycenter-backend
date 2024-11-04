from flask import Flask, request, jsonify
from flask_cors import CORS
from babycenter_backend.handler import RequestHandler
from babycenter_backend.user import User
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Optional
from werkzeug.datastructures import MultiDict
import json

handler = RequestHandler()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'placeholder'  # Necessary for WTForms
app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for API requests
CORS(app)  # This will enable CORS for all routes and origins

# Define WTForms forms for validation
class QueryForm(FlaskForm):
    user_id = StringField('user_id', validators=[DataRequired()])
    country = StringField('country', validators=[DataRequired()])
    startDate = StringField('startDate', validators=[DataRequired()])
    endDate = StringField('endDate', validators=[DataRequired()])
    keywords = StringField('keywords', validators=[Optional()])
    groups = StringField('groups', validators=[Optional()])
    num_comments = IntegerField('num_comments', validators=[DataRequired()])
    post_or_comment = StringField('post_or_comment', validators=[DataRequired()])
    num_documents = IntegerField('num_documents', validators=[DataRequired()])

class SaveForm(FlaskForm):
    type = StringField('type', validators=[DataRequired()])
    _id = StringField('_id', validators=[DataRequired()])
    content = StringField('content', validators=[DataRequired()])

class LoadForm(FlaskForm):
    user_id = StringField('user_id', validators=[DataRequired()])
    computed_type = StringField('computed_type', validators=[DataRequired()])

class NgramForm(FlaskForm):
    user_id = StringField('user_id', validators=[DataRequired()])
    startDate = StringField('startDate', validators=[DataRequired()])
    endDate = StringField('endDate', validators=[DataRequired()])
    keywords = StringField('keywords', validators=[Optional()])

@app.route('/query', methods=['GET'])
def query():
    form = QueryForm(request.args)
    if form.validate():
        try:
            user_id = form.user_id.data
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
                "user_id": user_id,
                "country": form.country.data,
                "startDate": form.startDate.data,
                "endDate": form.endDate.data,
                "keywords": form.keywords.data.split(',') if form.keywords.data else [],
                "groups": form.groups.data.split(',') if form.groups.data else [],
                "num_comments": form.num_comments.data,
                "post_or_comment": form.post_or_comment.data,
                "num_documents": form.num_documents.data
            }

            response = handler.handle(params)
            return jsonify({"user": user.id, "response": response})

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    else:
        return jsonify({"status": "error", "message": form.errors})
    
from werkzeug.datastructures import MultiDict
import json

@app.route('/save', methods=['POST'])
def save():
    try:
        # Extract JSON data from the request
        data = request.json
        print("Received Data:", data)  # Debugging output

        # Flatten the data for WTForms form processing
        val_data = {
            "type": data.get('type'),
            "_id": data.get('_id'),
            "content": json.dumps(data.get('content'))  # Convert content to string
        }

        print("Form Input Data:", val_data)  # Debugging output

        val_data['content'] = json.loads(val_data['content'])

        # Bind the flattened data to the form
        form = SaveForm(MultiDict(val_data))

        # Validate the form input
        if form.validate():
            # Construct the parameters
            params = {
                "request_type": "save",
                "user_id": data.get('userId'),
                "_id": val_data['_id'],
                "type": val_data['type'],
                "content": val_data['content']
            }

            # Pass the parameters to the handler
            handler.handle(params)

            return jsonify({"status": "success", "message": "Data saved successfully"})
        else:
            return jsonify({"status": "error", "message": form.errors})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

   


@app.route('/load', methods=['GET'])
def load():
    form = LoadForm(request.args)
    if form.validate():
        try: 
            params = {
                "request_type": "load",
                "user_id": form.user_id.data,
                "computed_type": form.computed_type.data,
            }

            response = handler.handle(params)
            return jsonify({"status": "success", "message": "Data loaded successfully", "content": response})

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    else:
        return jsonify({"status": "error", "message": form.errors})

@app.route('/ngram', methods=['GET'])
def ngram():
    form = NgramForm(request.args)
    if form.validate():
        try:
            params = {
                "request_type": "ngram",
                "user_id": form.user_id.data,
                "startDate": form.startDate.data,
                "endDate": form.endDate.data,
                "keywords": form.keywords.data.split(',') if form.keywords.data else []
            }

            response = handler.handle(params)

            return jsonify({"status": "success", "message": "Ngram computation successful", "content": response})

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    else:
        return jsonify({"status": "error", "message": form.errors})
