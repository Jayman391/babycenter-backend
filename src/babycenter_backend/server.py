from flask import Flask, request, jsonify
from flask_cors import CORS
from babycenter_backend.handler import RequestHandler
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField
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
    sessionID = FloatField('sessionID', validators=[DataRequired()])
    country = StringField('country', validators=[DataRequired()])
    startDate = StringField('startDate', validators=[DataRequired()])
    endDate = StringField('endDate', validators=[DataRequired()])
    keywords = StringField('keywords', validators=[Optional()])
    groups = StringField('groups', validators=[Optional()])
    num_comments = IntegerField('num_comments', validators=[DataRequired()])
    post_or_comment = StringField('post_or_comment', validators=[DataRequired()])
    num_documents = IntegerField('num_documents', validators=[DataRequired()])

class NgramForm(FlaskForm):
    sessionID = FloatField('sessionID', validators=[DataRequired()])
    startDate = StringField('startDate', validators=[DataRequired()])
    endDate = StringField('endDate', validators=[DataRequired()])
    keywords = StringField('keywords', validators=[Optional()])

@app.route('/query', methods=['GET'])
def query():
    form = QueryForm(request.args)
    if form.validate():
        try:
            # Construct params for handler
            params = {
                "request_type": "query",
                "sessionID": form.sessionID.data,
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
            return jsonify({"status": "success", "response": response})

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
                "sessionID": form.sessionID.data,
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
