from flask import Blueprint, request, jsonify
from app.models import user_model

users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/')
def home():
    return "User Management System"

@users_bp.route('/users', methods=['GET'])
def get_users():
    users = user_model.get_all_users()
    return jsonify(users), 200

@users_bp.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    user = user_model.get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

@users_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not all(k in data for k in ("name", "email", "password")):
        return jsonify({"error": "Missing fields"}), 400
    user_model.create_user(data["name"], data["email"], data["password"])
    return jsonify({"message": "User created"}), 201

@users_bp.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not data or not all(k in data for k in ("name", "email")):
        return jsonify({"error": "Invalid data"}), 400
    user_model.update_user(user_id, data["name"], data["email"])
    return jsonify({"message": "User updated"}), 200

@users_bp.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user_model.delete_user(user_id)
    return jsonify({"message": f"User {user_id} deleted"}), 200

@users_bp.route('/search', methods=['GET'])
def search_users():
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "Please provide a name to search"}), 400
    users = user_model.search_users_by_name(name)
    return jsonify(users), 200

@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not all(k in data for k in ("email", "password")):
        return jsonify({"error": "Invalid login data"}), 400
    user = user_model.login_user(data["email"], data["password"])
    if user:
        return jsonify({"status": "success", "user_id": user["id"]}), 200
    return jsonify({"status": "failed"}), 401
