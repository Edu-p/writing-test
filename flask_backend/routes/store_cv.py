from flask import request, jsonify, Blueprint
from db import db 
import PyPDF2
from io import BytesIO
import base64
from PyPDF2 import PdfReader

store_cv_bp = Blueprint('store_cv', __name__)

@store_cv_bp.route('/store_cv_db', methods=['POST'])
def store_cv_db(): 
    data = request.get_json()
    user_id = data['user_id']
    pdf_base64 = data['pdf_base64']

    if not pdf_base64:
        return jsonify({"error": "pdf not found"}), 404

    pdf_binary = base64.b64decode(pdf_base64)

    pdf_file = BytesIO(pdf_binary)

    reader = PdfReader(pdf_file)
    num_pages = len(reader.pages)
    pdf_text = ""
    for page_num in range(num_pages):
        page = reader.pages[page_num]
        pdf_text += page.extract_text()

    db.CVs.insert_one({
        "user_id": user_id,
        "pdf_text": pdf_text
    })

    return jsonify({"message": "PDF text stored"}), 200






