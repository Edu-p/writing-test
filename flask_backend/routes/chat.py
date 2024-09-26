from flask import request, jsonify, Blueprint
from db import db
from openai_client import client_openai
from utils.helpers import get_completion_from_messages

import pymongo

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['POST'])
def chat_response():
    data = request.get_json()
    user_id = data['user_id']
    thread_id = data['thread_id']
    content = data['content']

    conversations = db.Conversations.find({"thread_id": thread_id}).sort("_id", pymongo.ASCENDING)
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

    return jsonify({"response": response})