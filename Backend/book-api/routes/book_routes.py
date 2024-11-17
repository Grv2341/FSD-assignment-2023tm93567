from flask import Blueprint, jsonify, request
from services.book_service import create_book, get_book_query, get_book_id
import requests

book = Blueprint('book', __name__)

auth_url = "http://localhost:5000/auth/session" 

@book.route('/', methods=['POST'])
def create_user():
    if not validate_session(request.headers.get("session-id")):
        return jsonify({"meesage": "Not Authorized"}), 403
    data = request.get_json()
    response = create_book(data)
    return jsonify(response.body), response.status

@book.route("/query", methods = ['POST'])
def get_book_by_query():
    if not validate_session(request.headers.get("session-id")):
        return jsonify({"meesage": "Not Authorized"}), 403
    data = request.get_json()
    response = get_book_query(data)
    return jsonify(response.body), response.status

@book.route("/<string:bookId>", methods = ['GET'])
def get_book_by_id(bookId):
    if not validate_session(request.headers.get("session-id")):
        return jsonify({"meesage": "Not Authorized"}), 403
    response = get_book_id(bookId)
    return jsonify(response.body), response.status

def validate_session(sessionId):
    data = {
        "sessionId": sessionId
    }
    try:
        if sessionId != None:
            response = requests.post(auth_url, json=data)
            if response.status_code == 200:
                return True
            return False
    except Exception as e:
        print(str(e))
        return False

