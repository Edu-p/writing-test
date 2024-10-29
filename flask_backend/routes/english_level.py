from flask import request, jsonify, Blueprint
from db import db
from utils.helpers import get_completion_from_messages
import re
import json
import pymongo
from typing import List, Dict

english_level_bp = Blueprint('english_level', __name__)


def get_piece_eval(messages: List[Dict], pillar: str) -> str:
    prompt_english_level = f"""
        Based on the previous conversation, determine the user's CEFR level (A1, A2, ..., C2).

        To evaluate the user's level, consider ONLY the following criterion: {pillar}.

        Please think carefully to provide the most accurate answer.

        Format your response as a JSON object containing "CEFR" and "COT" (Chain of Thought).

        For example:

            {{"CEFR": "A1", "COT": "Based on {pillar}, in the second message you could improve..."}}

        or

            {{"CEFR": "C2", "COT": "Based on {pillar}, you have performed perfectly."}}

        Do not include any text outside of this JSON object; only provide the JSON.

        Make your response as brief as possible.
    """

    messages_pillar = messages.copy()

    messages_pillar.append({"role": "user", "content": prompt_english_level})

    response_pillar = get_completion_from_messages(messages_pillar)
    match_pillar = re.search(
        r'\{\s*"CEFR"\s*:\s*"[A-Z0-9]+"\s*,\s*"COT"\s*:\s*".*?"\s*\}', response_pillar, re.DOTALL)

    if match_pillar:
        response_pillar = match_pillar.group(0)
    else:
        return jsonify({"error": "Failed to extract JSON from response"}), 500

    response_dict_pillar = json.loads(response_pillar)

    return response_dict_pillar['CEFR']


@english_level_bp.route('/get_english_level', methods=['POST'])
def get_english_level():
    data = request.get_json()
    user_id = data['user_id']
    thread_id = data['thread_id']

    already_computed = db.EnglishLevel.find_one(
        {"thread_id": thread_id, "user_id": user_id})
    if already_computed:
        return jsonify({"COT": already_computed['COT'], "CEFR": already_computed['CEFR'], "CEFR_GS": already_computed['CEFR_GS'], "CEFR_VW": already_computed['CEFR_VW'], "CEFR_CC": already_computed['CEFR_CC'], "CEFR_CE": already_computed['CEFR_CE']})
    else:
        conversations = db.Conversations.find(
            {"thread_id": thread_id}).sort("_id", pymongo.ASCENDING)
        messages = [{"role": conv["role"], "content": conv["content"]}
                    for conv in conversations]

        eval_GS = get_piece_eval(messages=messages, pillar="Grammar and Syntax")
        eval_VW = get_piece_eval(messages=messages, pillar="Vocabulary and Word Choice")
        eval_CC = get_piece_eval(messages=messages, pillar="Coherence and Cohesion")
        eval_CE = get_piece_eval(messages=messages, pillar="Clarity of Expressions")

        # print(f"eval_GS: {eval_GS}, eval_VW: {eval_VW}, eval_CC: {eval_CC}, eval_CE: {eval_CE}")

        prompt_english_level = f"""
            Based on the previous conversation, identify the final CEFR level (A1, A2, ..., C2) of User(just eval according to "user" disregard the "system" messages). 

            We have specialist evaluations for this conversation in four pillars:
            - "Grammar and Syntax": {eval_GS}
            - "Vocabulary and Word Choice": {eval_VW}
            - "Coherence and Cohesion": {eval_CC}
            - "Clarity of Expression": {eval_CE}

            Please leverage these grades and consider the entire conversation to determine the final CEFR level.

            Think carefully to provide the most accurate answer.

            Format your response as a JSON object containing "CEFR" and "COT" (Chain of Thought).

            For example:
            {{"CEFR": "A1", "COT": "In the second message, you typed 'jst' instead of 'just'."}}
            or
            {{"CEFR": "C2", "COT": "Based on all pillars, you have performed perfectly."}}

            Do not include any additional text outside of this JSON object.

            Make your response as concise as possible.
        """

        messages = messages.copy()

        messages.append({"role": "user", "content": prompt_english_level})

        response = get_completion_from_messages(messages)
        match = re.search(
            r'\{\s*"CEFR"\s*:\s*"[A-Z0-9]+"\s*,\s*"COT"\s*:\s*".*?"\s*\}', response, re.DOTALL)

        if match:
            response = match.group(0)
        else:
            return jsonify({"error": "Failed to extract JSON from response"}), 500

        response_dict = json.loads(response)

        response_dict["CEFR_GS"] = eval_GS
        response_dict["CEFR_VW"] = eval_VW
        response_dict["CEFR_CC"] = eval_CC
        response_dict["CEFR_CE"] = eval_CE


        db.EnglishLevel.insert_one({
            "thread_id": thread_id,
            "user_id": user_id,
            "CEFR": response_dict['CEFR'],
            "CEFR_GS": eval_GS,
            "CEFR_VW": eval_VW,
            "CEFR_CC": eval_CC,
            "CEFR_CE": eval_CE,
            "COT": response_dict['COT']
        })

        return jsonify(response_dict)


@english_level_bp.route('/max_english_level', methods=['POST'])
def max_english_level():
    data = request.get_json()
    user_id = data['user_id']

    levels_of_user = db.EnglishLevel.find(
        {"user_id": user_id}).sort("_id", pymongo.ASCENDING)

    CEFR_order = ["A1", "A2", "B1", "B2", "C1", "C2"]

    CEFRs = [level['CEFR'] for level in levels_of_user]

    if CEFRs:
        max_CEFR = max(CEFRs, key=lambda CEFR: CEFR_order.index(CEFR))
        return jsonify({"max_CEFR": max_CEFR})
    else:
        return jsonify({"error": "No CEFR levels found for the user"}), 404
