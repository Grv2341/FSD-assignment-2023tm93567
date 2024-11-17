from flask import Blueprint, jsonify, request
from services.auth_service import authenticate_user, authenticate_session

auth = Blueprint('auth', __name__)

@auth.route('/user', methods=['POST'])
def auth_user():
    data = request.get_json()
    response = authenticate_user(data)
    return jsonify(response.body), response.status

@auth.route('/session', methods=['POST'])
def auth_session():
    data = request.get_json()
    response = authenticate_session(data)
    return jsonify(response.body), response.status


