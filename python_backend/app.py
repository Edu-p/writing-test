from flask import Flask, request, jsonify, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from pymongo import MongoClient
from openai import OpenAI
import os
from dotenv import load_dotenv
import logging 
import uuid

load_dotenv()

app = Flask(__name__)

CORS(app)

# setup mongo and open ai api key
MONGO_URI = os.getenv('MONGO_URI')
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
client = MongoClient(MONGO_URI)
db = client.myDatabase

client_openai = OpenAI()

# serve swagger ui
SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Chat API"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# helper functions 
def get_completion_from_messages(messages, model='gpt-4o-mini'):
    completion = client_openai.chat.completions.create(
        model=model,
        messages=messages
    )
    return completion.choices[0].message.content

# routes
@app.route('/auth', methods=['POST'])
def auth(): 
    """
        POST in (1).0
    """
    data = request.get_json()
    email = data['email']
    password = data['password']
    
    user = db.Users.find_one({"email": email, "password": password})
    
    if user:
        user_id = user["user_id"]
        return jsonify({"user_id": user_id})
    else:
        return jsonify({"error": "Invalid credentials"})

@app.route('/explanations', methods=['POST'])
def get_explanation():
    """
        POST in (5).0 
    """
    



@app.route('/chat', methods=['POST'])
def chat_response():
    """
        POST in (5).1
    """
    data = request.get_json()
    user_id = data['user_id']
    thread_id = data['thread_id']
    content = data['content']

    conversations = db.Conversations.find({"thread_id": thread_id}).sort("_id", 1)
    messages = [{"role": conv["role"], "content": conv["content"]} for conv in conversations]

    messages.append({"role": "user", "content": content})

    response = get_completion_from_messages(messages)

    db.Conversations.insert_many([
        {
            "thread_id": thread_id,
            "user_id": user_id,
            "role": "user",
            "content": content
        },
        {
            "thread_id": thread_id,
            "user_id": user_id,
            "role": "assistant",
            "content": response
        }
    ])

    # print(list(db.Conversations.find()))

    return jsonify({"response": response})

@app.route('/get_conversation', methods=['GET'])
def get_conversation():
    """
        GET in (5).1
    """
    thread_id = str(uuid.uuid4())
    return jsonify({"thread_id": thread_id})

@app.route('/swagger.json')
def swagger_json():
    return send_from_directory('static', 'swagger.json')

if __name__ == '__main__':
    app.run(debug=True)
