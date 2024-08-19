from flask import Flask, request, jsonify, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from pymongo import MongoClient, ASCENDING
import pymongo
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
    data = request.get_json()
    type_of_test = data['type']

    explanation = db.Explanations.find_one({"type": type_of_test})

    if explanation:
        explanation_to_return = explanation["explanation"]
        return jsonify({"explanation": explanation_to_return})
    else:
        return jsonify({"error": "Type of test not found"})




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

@app.route('/get_conversation', methods=['POST'])
def get_conversation():
    """
        POST in (5).1
    """
    data = request.get_json()
    user_id = data['user_id']
    type_of_test = data['type_of_test']

    thread_id = str(uuid.uuid4())

    if (type_of_test == 'report'):
        # TODO: improve instantiation of this prompt
        prompt = """
            You are a tech lead. The purpose of this conversation is to collect a detailed report from your software engineer. Think about the better type of question that you can ask to gather comprehensive information about their activities, progress, challenges, and any support they might need. \
            Please, be short as possible on your responses.
        """
        
        db.Conversations.insert_one({
            "thread_id": thread_id,
            "user_id": user_id,
            "role": "system",
            "content": prompt
        })
    else:   
        return jsonify({"error": "Type of test not found"})

    return jsonify({"thread_id": thread_id})

@app.route('/get_english_level', methods=['POST'])
def get_english_level():
    data = request.get_json()
    user_id = data['user_id']
    thread_id = data['thread_id']

    conversations = db.Conversations.find({"thread_id": thread_id}).sort("_id", pymongo.ASCENDING)
    
    messages = [{"role": conv["role"], "content": conv["content"]} for conv in conversations]

    prompt_english_level = """
        Identify the items based on previous conversation:
            - Level of english(0% min and 100% max)
            - CEPR(A1, A2,..., C2)
        
        To evaluate the level of user you can think in these criteria "Grammar and Syntax", "Vocabulary and Word Choice", "Coherence and Cohesion", "Clarity of Expression", "Task Achievement". \
        Format your response as a JSON object with \
        "level" and "CEPR". \
        I don't want you to send any other token outside of this json, just the json. \
        Make your response as short as possible.
    """

    messages.append({"role": "user", "content": prompt_english_level})

    response = get_completion_from_messages(messages)

    return response 

@app.route('/swagger.json')
def swagger_json():
    return send_from_directory('static', 'swagger.json')

if __name__ == '__main__':
    app.run(debug=True)
