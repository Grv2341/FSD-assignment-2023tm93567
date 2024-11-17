from flask import Blueprint, jsonify, request
from services.user_service import create_user_db, get_user

user = Blueprint('user', __name__)

@user.route('/create', methods=['POST'])
def create_user():
    data = request.get_json()
    response = create_user_db(data)
    return jsonify(response.body), response.status

@user.route('/<string:userId>', methods=['GET'])
def get_user_by_id(userId):
    response = get_user(userId)
    return jsonify(response.body), response.status