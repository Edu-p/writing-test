from flask import request, jsonify, Blueprint
from db import db
from openai_client import client_openai
from utils.helpers import get_completion_from_messages
from llama_index.core.indices.vector_store import VectorStoreIndex
from llama_index.core.readers.file.base import SimpleDirectoryReader
from llama_index.core import Document
from llama_index.core.node_parser.text.sentence_window import SentenceWindowNodeParser
from llama_index.core.postprocessor import MetadataReplacementPostProcessor
import json
import re

from llama_index.core import Settings

from llama_index.llms.openai.base import OpenAI

from llama_index.embeddings.openai import OpenAIEmbedding

import pymongo

from deepeval.integrations.llama_index import DeepEvalAnswerRelevancyEvaluator
from deepeval.integrations.llama_index import DeepEvalFaithfulnessEvaluator
from deepeval.integrations.llama_index import DeepEvalContextualRelevancyEvaluator

from deepeval.metrics import AnswerRelevancyMetric

from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric

from deepeval import evaluate

import nest_asyncio

# avoiding conflicts with event loop(due to deepeval methods)
nest_asyncio.apply()

# basic llm setup
llm = OpenAI(model='gpt-4o-mini')
embed_model = OpenAIEmbedding(model="text-embedding-3-small")

Settings.llm = llm
Settings.embed_model = embed_model

# node parser(sentence window approach)
node_parser = SentenceWindowNodeParser.from_defaults(
    window_size=3,
    window_metadata_key='window',
    original_text_metadata_key='original_text',
)

# helper functions


def reconstruct_index(index_data):
    documents = [Document(text=doc['text']) for doc in index_data['documents']]
    nodes = node_parser.get_nodes_from_documents(documents)
    index = VectorStoreIndex(nodes)
    return index


def store_index(index, user_id, thread_id, index_type):
    index_data = {
        'user_id': user_id,
        'thread_id': thread_id,
        'type': index_type,
        # check if this acess is correct
        'documents': [{'text': node.metadata['original_text']} for node in index.docstore.docs.values()],
    }
    db.QueryEngines.insert_one(index_data)


def create_interview_questions_index():
    documents = SimpleDirectoryReader(
        # non-unix based path
        input_files=["./utils/common_questions.txt"]
    ).load_data()
    nodes = node_parser.get_nodes_from_documents(documents)
    index = VectorStoreIndex(nodes)
    return index


def create_cv_index(user_id: str):
    cv_data = db.CVs.find_one({'user_id': user_id})
    document = Document(text=cv_data['pdf_text'])
    nodes = node_parser.get_nodes_from_documents([document])
    index = VectorStoreIndex(nodes)
    return index


def generate_final_message(best_question: str, best_context: str, content: str, messages: list, thread_id: str, user_id: str) -> str:
    prompt = f"""
        You are a virtual interviewer simulating a technical interview.

        User's last message (delimited by next -> <-):
        -> {content} <-

        Based on the best question (delimited by next -> <-):
        -> {best_question} <-

        And the best context from the user's CV (delimited by next -> <-):
        -> {best_context} <-

        Generate a brief discussion about what was talked about, and then present the next question (best question) incorporating the context from the CV. This will be your "response". If the best question or best context doesn't make sense, just ignore them. 

        Additionally, provide the next logical message of the conversation and a text correcting ALL my errors, such as verb tenses(just according at to "User's last message"). For example, "You wrote 'I need to do a conversation with you.' A more natural way to say this is 'I need to have a conversation with you.'"

        Format your response as a JSON object with "response" and "corr". 

        Before give the final answer think a while and do not include any other tokens outside of this JSON, in this json just these 2 KEYS("response" and "corr"). Make your response as concise as possible.
    """
    messages.append({"role": "user", "content": prompt})

    response = get_completion_from_messages(messages)

    # print(f"Generated response: {response}")

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

    # print(f"AR: {evaluation[0].metrics_data[0].score}")

    db.Evals.insert_one({
            "entity": "final_entity",
            "thread_id": thread_id,
            "user_id": user_id,
            "cr": 0,
            "ar": evaluation[0].metrics_data[0].score,
            "f": 0,
    })

    return response


interview_bp = Blueprint('interview', __name__)


@interview_bp.route('/interview_chat', methods=['POST'])
def interview_chat_gen():
    data = request.get_json()
    user_id = data['user_id']
    thread_id = data['thread_id']
    content = data['content']

    # ar_evaluator = DeepEvalAnswerRelevancyEvaluator()
    # f_evaluator = DeepEvalFaithfulnessEvaluator()
    # cr_evaluator = DeepEvalContextualRelevancyEvaluator()

    if not all([data, user_id, content]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # interview question index
        interview_index_data = db.QueryEngines.find_one({
            'user_id': user_id,
            'thread_id': thread_id,
            'type': 'interview_questions'
        })

        if interview_index_data:
            interview_index = reconstruct_index(interview_index_data)

        else:
            interview_index = create_interview_questions_index()
            store_index(interview_index, user_id,
                        thread_id, 'interview_questions')

        cv_index_data = db.QueryEngines.find_one({
            'user_id': user_id,
            'thread_id': thread_id,
            'type': 'user_cv'
        })

        if cv_index_data:
            cv_index = reconstruct_index(cv_index_data)
        else:
            cv_index = create_cv_index(user_id)

        conversations = db.Conversations.find(
            {"thread_id": thread_id}).sort("_id", pymongo.ASCENDING)
        messages = [{"role": conv["role"], "content": conv["content"]}
                    for conv in conversations]

        prompt_retrieve_question = f"""
        User's last message (delimited by next -> <-):
        -> {content} <-

        According to this message, please give me the most appropriate question to ask next. Please, be brief and to the point.
        """

        best_question_response = interview_index.as_query_engine(
            similarity_top_k=4,
            node_postprocessor=[MetadataReplacementPostProcessor(
                target_metadata_key='window')]
        ).query(prompt_retrieve_question)

        # cr_evaluation_result = cr_evaluator.evaluate_response(
        #     query=content, response=best_question_response)
        # ar_evaluation_result = ar_evaluator.evaluate_response(
        #     query=content, response=best_question_response)
        # f_evaluation_result = f_evaluator.evaluate_response(
        #     query=content, response=best_question_response)

        # db.Evals.insert_one({
        #     "entity": "interview_index",
        #     "thread_id": thread_id,
        #     "user_id": user_id,
        #     "cr": cr_evaluation_result.score,
        #     "ar": ar_evaluation_result.score,
        #     "f": f_evaluation_result.score,
        # })

        best_question = str(best_question_response)

        prompt_retrieve_context_cv = f"""
        User's last message (delimited by next -> <-):
        -> {content} <-

        Best question to ask in a interview according this last message(delimited by next -> <-):
        -> {best_question} <-

        According to this message, please give me the most appropriate context about CV, it can be other experience in other place that are related for example. Please be brief and to the point.
        """

        best_context_response = cv_index.as_query_engine(
            similarity_top_k=4,
            node_postprocessor=[MetadataReplacementPostProcessor(
                target_metadata_key='window')]
        ).query(prompt_retrieve_context_cv)

        best_context = str(best_context_response)

        # cr_evaluation_result = cr_evaluator.evaluate_response(
        #     query=content, response=best_question_response)
        # ar_evaluation_result = ar_evaluator.evaluate_response(
        #     query=content, response=best_question_response)
        # f_evaluation_result = f_evaluator.evaluate_response(
        #     query=content, response=best_question_response)

        # db.Evals.insert_one({
        #     "entity": "cv_index",
        #     "thread_id": thread_id,
        #     "user_id": user_id,
        #     "cr": cr_evaluation_result.score,
        #     "ar": ar_evaluation_result.score,
        #     "f": f_evaluation_result.score,
        # })

        response = generate_final_message(
            best_question, best_context, content, messages, thread_id, user_id
        )

        match = re.search(
            r'\{\s*"response"\s*:\s*".*"\s*,\s*"corr"\s*:\s*".*"\s*\}', response, re.DOTALL)

        if match:
            response_json = match.group(0)
            # print(f"Extracted JSON: {response_json}")
            response_dict = json.loads(response_json)
        else:
            # print("No match found")
            # Handle the error appropriately
            return jsonify({"error": "Failed to parse response from AI assistant."}), 500


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

    except Exception as e:
        return jsonify({'error': str(e)}), 500
