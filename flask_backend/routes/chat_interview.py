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

interview_bp = Blueprint('interview', __name__)

@interview_bp.route('/interview_chat', methods=['POST'])
def interview_chat_gen():
    data = request.get_json()
    user_id = data['user_id']
    thread_id = data['thread_id']
    content = data['content']


    # basic llm setup 
    llm = OpenAI(model='gpt-4')
    embed_model = OpenAIEmbedding(model="text-embedding-3-small")
    
    
    Settings.llm = llm
    Settings.embed_model = embed_model

    # node parser(sentence window approach)
    node_parser = SentenceWindowNodeParser.from_defaults(
        window_size = 3,
        window_metadata_key='window',
        original_text_metadata_key='original_text',
    )
