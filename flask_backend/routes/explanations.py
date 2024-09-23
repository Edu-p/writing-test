from flask import request, jsonify
from . import explanations_bp
from app import db

@explanations_bp.route('/explanations', methods=['POST'])
def get_explanation():
    data = request.get_json()
    type_of_test = data['type']

    explanation = db.Explanations.find_one({"type": type_of_test})

    if explanation:
        explanation_to_return = explanation["explanation"]
        return jsonify({"explanation": explanation_to_return})
    else:
        return jsonify({"error": "Type of test not found"})