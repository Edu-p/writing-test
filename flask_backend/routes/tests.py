from flask import request, jsonify, Blueprint
from db import db
import pymongo

tests_bp = Blueprint('tests', __name__)


@tests_bp.route('/return_all_tests', methods=['POST'])
def return_all_tests():
    data = request.get_json()
    user_id = data['user_id']
    grades = db.EnglishLevel.find(
        {"user_id": user_id}).sort("_id", pymongo.ASCENDING)

    grades_list = []
    for grade in grades:
        grades_list.append(grade['CEPR'])

    return jsonify(grades_list), 200
