from flask import request, jsonify, Blueprint
from db import db
import pymongo
from statistics import mean

eval_bp = Blueprint('evals', __name__)

@eval_bp.route('/evals', methods=['POST'])
def get_evals():
    data = request.get_json()
    user_id = data['user_id']

    evals = db.Evals.find({"user_id": user_id}).sort("_id", pymongo.ASCENDING)
    

    evals_ar = [s_eval['ar'] for s_eval in evals]
    if evals_ar:
        mean_ar = mean(evals_ar)
    else:
        mean_ar = None

    return jsonify({"mean_ar": mean_ar}), 200
