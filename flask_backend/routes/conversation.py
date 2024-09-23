from flask import request, jsonify
from . import conversation_bp
from app import db
import uuid

@conversation_bp.route('/get_conversation', methods=['POST'])
def get_conversation():
    data = request.get_json()
    user_id = data['user_id']
    type_of_test = data['type_of_test']

    thread_id = str(uuid.uuid4())

    if type_of_test == 'report':
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