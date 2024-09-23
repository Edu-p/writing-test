from flask import request, jsonify
from . import tests_bp
from app import db

@tests_bp.route('/return_all_tests', methods=['POST'])
def return_all_tests():
    data = request.get_json()
    user_id = data['user_id']
    grades = db.EnglishLevel.find({"user_id": user_id}).sort("_id", pymongo.ASCENDING)

    grades_list = []
    for grade in grades:
        grades_list.append(grade['CEPR'])

    return jsonify(grades_list), 200