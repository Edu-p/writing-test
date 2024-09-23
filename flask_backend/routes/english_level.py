from flask import request, jsonify
from . import english_level_bp
from app import db, client_openai
from utils.helpers import get_completion_from_messages
import re
import json

@english_level_bp.route('/get_english_level', methods=['POST'])
def get_english_level():
    data = request.get_json()
    user_id = data['user_id']
    thread_id = data['thread_id']
    
    already_computed = db.EnglishLevel.find_one({"thread_id": thread_id, "user_id": user_id})
    if already_computed:
        return jsonify({"level": already_computed['level'], "CEPR": already_computed['CEPR']})
    else:
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

        match = re.search(r'\{\s*"level"\s*:\s*\d+\s*,\s*"CEPR"\s*:\s*"[A-Z0-9]+"\s*\}', response, re.DOTALL)

        if match:
            response_json = match.group(0)
        else:
            return jsonify({"error": "Failed to extract JSON from response"}), 500

        response_dict = json.loads(response_json)
        
        db.EnglishLevel.insert_one({
            "thread_id": thread_id,
            "user_id": user_id,
            "level": response_dict['level'],
            "CEPR": response_dict['CEPR']
        })

        return jsonify(response_dict)

@english_level_bp.route('/max_english_level', methods=['POST'])
def max_english_level():
    data = request.get_json()
    user_id = data['user_id']

    levels_of_user = db.EnglishLevel.find({"user_id": user_id}).sort("_id", pymongo.ASCENDING)

    cepr_order = ["A1", "A2", "B1", "B2", "C1", "C2"]

    ceprs = [level['CEPR'] for level in levels_of_user]

    if ceprs:
        max_cepr = max(ceprs, key=lambda cepr: cepr_order.index(cepr))
        return jsonify({"max_cepr": max_cepr})
    else:
        return jsonify({"error": "No CEPR levels found for the user"}), 404