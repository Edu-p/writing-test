from routes.chat_interview import interview_bp
from routes.store_cv import store_cv_bp
from routes.tests import tests_bp
from routes.english_level import english_level_bp
from routes.conversation import conversation_bp
from routes.chat import chat_bp
from routes.explanations import explanations_bp
from routes.auth import auth_bp
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from pymongo import MongoClient
from openai_client import client_openai
from dotenv import load_dotenv
import os
from db import db


load_dotenv()

app = Flask(__name__)
CORS(app)

# setup mongo and open ai api key
MONGO_URI = os.getenv('MONGO_URI')
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
client = MongoClient(MONGO_URI)
db = db

client_openai = client_openai

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(explanations_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(conversation_bp)
app.register_blueprint(english_level_bp)
app.register_blueprint(tests_bp)
app.register_blueprint(store_cv_bp)
app.register_blueprint(interview_bp)

# serve swagger ui
SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={'app_name': "Chat API"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


# health check route
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200


@app.route('/swagger.json')
def swagger_json():
    return send_from_directory('static', 'swagger.json')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
