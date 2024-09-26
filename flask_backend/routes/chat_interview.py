from flask import request, jsonify, Blueprint
from db import db
from openai_client import client_openai
from utils.helpers import get_completion_from_messages
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Document,
    SentenceWindowNodeParser,
    MetadataReplacementPostProcessor
)

from llama_index.core import Settings

from llama_index.llms.openai.base import OpenAI

from llama_index.embeddings.openai import OpenAIEmbedding

# basic llm setup 
llm = OpenAI(model='gpt-4')
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
        input_files=["../utils/common_questions.txt"]
    ).load_data()
    nodes = node_parser.get_nodes_from_documents(documents)
    index = VectorStoreIndex(nodes)
    # does not need .asqueryengine?
    return index

def create_cv_index(user_id):
    cv_data = db.CVs.find_one({'user_id': user_id})
    document = Document(text=cv_data['pdf_text'])
    nodes = node_parser.get_nodes_from_documents([document])
    index = VectorStoreIndex(nodes)
    return index

def generate_final_message(best_question, best_context, content, messages):
    prompt = f"""
        You are a virtual interviewer simulating a technical interview.

        User's last message:
        {content}

        Based on the best question:
        {best_question}

        And the best context from the user's CV:
        {best_context}

        Generate a brief discussion about what was talked about, and then present the next question(try to incorporate the context from the CV).
    """
    messages.append({"role": "user", "content": prompt})

    response = get_completion_from_messages(messages)

interview_bp = Blueprint('interview', __name__)

@interview_bp.route('/interview_chat', methods=['POST'])
def interview_chat_gen():
    data = request.get_json()
    user_id = data['user_id']
    thread_id = data['thread_id']
    content = data['content']
    
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
            store_index(interview_index, user_id, thread_id, 'interview_questions') 
        
        cv_index_data = db.QueryEngines.find_one({
            'user_id': user_id,
            'thread_id': thread_id,
            'type': 'user_cv'
        })

        if cv_index_data:
            cv_index = reconstruct_index(cv_index_data)
        else:  
            cv_index = create_cv_index(user_id)

        conversations = db.Conversations.find({"thread_id": thread_id}).sort("_id", pymongo.ASCENDING)
        messages = [{"role": conv["role"], "content": conv["content"]} for conv in conversations]

        best_question_response = interview_index.query(content)
        best_question = str(best_question_response)

        best_context_response = cv_index.query(content)
        best_context = str(best_context_response)

        final_message_from_llm = generate_final_message(
            best_question, best_context, content 
        )

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
            "content": final_message_from_llm
        }
        ])

        return jsonify({'response': final_message_from_llm})


    except Exception as e:
        return jsonify({'error': str(e)}), 500
