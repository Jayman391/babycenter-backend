import os
from flask import Flask, request, jsonify
from flask_cors import CORS

import sys 
# add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from src.babycenter_backend.handler import RequestHandler

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField
from wtforms.validators import DataRequired, Optional
import logging

# Initialize handler
handler = RequestHandler()

# Initialize Flask app
app = Flask(__name__)

# Load configuration from environment variables
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'fallback-secret-key')
app.config['WTF_CSRF_ENABLED'] = False  # Consider enabling CSRF in production for sensitive forms

# Configure CORS
CORS(app, resources={r"/api/*": {"origins": os.getenv('CORS_ALLOWED_ORIGINS', '*').split(',')}})

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# Define WTForms forms for validation
class QueryForm(FlaskForm):
    sessionID = FloatField('sessionID', validators=[DataRequired()])
    country = StringField('country', validators=[DataRequired()])
    startDate = StringField('startDate', validators=[Optional()])
    endDate = StringField('endDate', validators=[Optional()])
    keywords = StringField('keywords', validators=[Optional()])
    groups = StringField('groups', validators=[Optional()])
    num_comments = IntegerField('num_comments', validators=[DataRequired()])
    post_or_comment = StringField('post_or_comment', validators=[DataRequired()])
    num_documents = IntegerField('num_documents', validators=[DataRequired()])

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
                "num_documents": form.num_documents.data,
                "nodate": False
            }

            response = handler.handle(params)
            return jsonify({"status": "success", "response": response})

        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return jsonify({"status": "process error", "message": str(e)})
    else:
        return jsonify({"status": "form error", "message": form.errors})

class NgramForm(FlaskForm):
    sessionID = FloatField('sessionID', validators=[DataRequired()])
    startDate = StringField('startDate', validators=[DataRequired()])
    endDate = StringField('endDate', validators=[DataRequired()])
    keywords = StringField('keywords', validators=[Optional()])

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
            logger.error(f"Error processing ngram: {str(e)}")
            return jsonify({"status": "process error", "message": str(e)})
    else:
        return jsonify({"status": "form error", "message": form.errors})

class AllotaxForm(FlaskForm):
    sessionID = FloatField('sessionID', validators=[DataRequired()])
    alpha = FloatField('alpha', validators=[DataRequired()])
    groups = StringField('groups', validators=[DataRequired()])

@app.route('/allotax', methods=['GET'])
def allotax():
    form = AllotaxForm(request.args)
    if form.validate():
        try:
            params = {
                "request_type": "allotax",
                "sessionID": form.sessionID.data,
                "alpha": form.alpha.data,
                "groups": form.groups.data.split(',')
            }

            response = handler.handle(params)

            return jsonify({"status": "success", "message": "Allotax computation successful", "content": response})

        except Exception as e:
            logger.error(f"Error processing allotax: {str(e)}")
            return jsonify({"status": "process error", "message": str(e)})
    else:
        return jsonify({"status": "form error", "message": form.errors})

if __name__ == '__main__':
    # Use a production WSGI server like Gunicorn in production instead of this
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8000)), debug=False)
