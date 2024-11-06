from flask import request, jsonify, Blueprint
from db import db
from openai_client import client_openai
from utils.helpers import get_completion_from_messages
import re
import json
import pymongo

from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric

from deepeval import evaluate 

import nest_asyncio

# avoiding conflicts with event loop(due to deepeval methods)
nest_asyncio.apply()

chat_bp = Blueprint('chat', __name__)


def generate_final_message(content: str, messages: list, thread_id: str, user_id: str) -> str:
    prompt = f"""
        You are a tech lead. The purpose of this conversation is to collect a detailed report from your software engineer. Think about the better type of question that you can ask to gather comprehensive information about their activities, progress, challenges, and any support they might need.             Please, be short as possible on your responses. \
        In addition i want to receive the next logic message of conversation and one text correcting ALL my errors. Like verb tenses,... \
        Example of correction: "You wrote "I need to do a conversation with you." A more natural way to say this is "I need to have a conversation with you."" \
        Format your response as a JSON object with "response" and "corr" \
        I don't want you to send any other token outside of this json, just the json. \
        Make your response as short as possible.

        User's last message:
        {content}
    """
    messages.append({"role": "user", "content": prompt})

    response = get_completion_from_messages(messages)

    metric = AnswerRelevancyMetric(
        threshold=0.7,
        model="gpt-4o-mini",
        include_reason=False,
        async_mode=False
    )

    test_case = LLMTestCase(
        input=prompt,
        actual_output=response
    )

    evaluation = evaluate([test_case], [metric])

    db.Evals.insert_one({
        "entity": "final_entity",
        "thread_id": thread_id,
        "user_id": user_id,
        "cr": 0,
        "ar": evaluation[0].metrics_data[0].score,
        "f": 0,
    })

    return response


@chat_bp.route('/chat', methods=['POST'])
def chat_response():
    data = request.get_json()
    user_id = data['user_id']
    thread_id = data['thread_id']
    content = data['content']

    print(f"THREAD ID -> {thread_id}")

    conversations = db.Conversations.find(
        {"thread_id": thread_id}).sort("_id", pymongo.ASCENDING)
    messages = [{"role": conv["role"], "content": conv["content"]}
                for conv in conversations]

    messages.append({"role": "user", "content": content})

    response = generate_final_message(content, messages, thread_id, user_id)
    
    match = re.search(
        r'\{\s*"response"\s*:\s*".*"\s*,\s*"corr"\s*:\s*".*"\s*\}', response, re.DOTALL)

    if match:
        response_json = match.group(0)
        print(f"Extracted JSON: {response_json}")
    else:
        print("No match found")

    response_dict = json.loads(response_json)

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
            "content": response_dict['response']
        }
    ])

    return jsonify({"response": response_dict['response'], "corr": response_dict['corr']})
