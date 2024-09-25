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
        input_files=["../utils/common_questions.txt"]
    ).load_data()
    nodes = node_parser.get_nodes_from_documents(documents)
    index = VectorStoreIndex(nodes)
    return index

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

        


    except:
