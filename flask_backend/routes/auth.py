from flask import request, jsonify
from . import auth_bp
from app import db

@auth_bp.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()
    email = data['email']
    password = data['password']
    
    user = db.Users.find_one({"email": email, "password": password})
    
    if user:
        user_id = user["user_id"]
        return jsonify({"user_id": user_id}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 404