from flask import request, jsonify, Blueprint
from db import db
from utils.helpers import get_completion_from_messages
import re
import json
import pymongo

english_level_bp = Blueprint('english_level', __name__)


@english_level_bp.route('/get_english_level', methods=['POST'])
def get_english_level():
    data = request.get_json()
    user_id = data['user_id']
    thread_id = data['thread_id']

    already_computed = db.EnglishLevel.find_one(
        {"thread_id": thread_id, "user_id": user_id})
    if already_computed:
        return jsonify({"COT": already_computed['COT'], "CEPR": already_computed['CEPR']})
    else:
        conversations = db.Conversations.find(
            {"thread_id": thread_id}).sort("_id", pymongo.ASCENDING)
        messages = [{"role": conv["role"], "content": conv["content"]}
                    for conv in conversations]

        prompt_english_level = """
            Identify the items based on previous conversation:
            - CEPR(A1, A2,..., C2)
            
            To evaluate the level of user you can think in these criteria "Grammar and Syntax", "Vocabulary and Word Choice", "Coherence and Cohesion", "Clarity of Expression", "Task Achievement". \
            Format your response as a JSON object with "CEPR" and "COT". \
            for example: {"CEPR":"A1", "COT": "In second message you typed wrong jst and the correct is just"} or {"CEPR":"C2", "COT": "based on "Grammar and Syntax", "Vocabulary and Word Choice", "Coherence and Cohesion", "Clarity of Expression", "Task Achievement" you have done all perfectly"} or... \
            I don't want you to send any other token outside of this json, just the json. \
            Make your response as short as possible.
        """

        messages.append({"role": "user", "content": prompt_english_level})

        response = get_completion_from_messages(messages)

        match = re.search(
            r'\{\s*"CEPR"\s*:\s*"[A-Z0-9]+"\s*,\s*"COT"\s*:\s*".*?"\s*\}', response, re.DOTALL)

        if match:
            response_json = match.group(0)
        else:
            return jsonify({"error": "Failed to extract JSON from response"}), 500

        response_dict = json.loads(response_json)

        db.EnglishLevel.insert_one({
            "thread_id": thread_id,
            "user_id": user_id,
            "CEPR": response_dict['CEPR'],
            "COT": response_dict['COT']
        })

        return jsonify(response_dict)


@english_level_bp.route('/max_english_level', methods=['POST'])
def max_english_level():
    data = request.get_json()
    user_id = data['user_id']

    levels_of_user = db.EnglishLevel.find(
        {"user_id": user_id}).sort("_id", pymongo.ASCENDING)

    cepr_order = ["A1", "A2", "B1", "B2", "C1", "C2"]

    ceprs = [level['CEPR'] for level in levels_of_user]

    if ceprs:
        max_cepr = max(ceprs, key=lambda cepr: cepr_order.index(cepr))
        return jsonify({"max_cepr": max_cepr})
    else:
        return jsonify({"error": "No CEPR levels found for the user"}), 404
