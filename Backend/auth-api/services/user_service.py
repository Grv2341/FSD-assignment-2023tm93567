import re
from models.response import Response
from models.user import User
from db import get_db_connection
from werkzeug.security import generate_password_hash
import time
import random
import uuid

email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
password_regex = r'^(?=.*[A-Z])(?=.*[\W_]).{8,}$'

def create_user_db(data):

    if not validateUserData(data):
        return Response({"message": "Invalid Data"}, 400)
    
    if check_duplicate_email(data["email"]):
        return Response({"message": "Email already exists"}, 400)
    
    conn = get_db_connection()
    hashed_password = generate_password_hash(data["password"])

    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (id, email, password, firstName, lastName) VALUES (?, ?, ?, ?, ?)',(str(uuid.uuid4()), data["email"], hashed_password, data["firstName"], data["lastName"]))
        conn.commit()
        payload = {
            "message": "User Registered Succesfully."
        }
        return Response(payload, 201)
    except Exception as e:
        print(str(e))
        return Response({"error": "Internal server error"}, 500)
    finally:
        conn.close()

def get_user(userId):
    if len(userId.strip()) <=0:
        return Response({"message": "Invalid Data"}, 400)
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (userId,))
        user = cursor.fetchone()
        if user:
            return Response(User.from_row(user).to_json(), 200)
        return Response({"message": "Not Found"}, 404)
    except Exception as e:
        print(str(e))
        return Response({"error": "Internal server error"}, 500)
    finally:
        conn.close()

def validateUserData(data):
    if "firstName" not in data or len(data["firstName"].strip()) <= 0 or not data["firstName"].strip().isalpha():
        return False
    if "lastName" not in data or len(data["lastName"].strip()) <= 0 or not data["lastName"].strip().isalpha():
        return False
    if "email" not in data or not re.match(email_regex, data["email"]):
        return False
    if "password" not in data or not re.match(password_regex, data["password"]):
        return False
    return True

def check_duplicate_email(email):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        if user:
            return True
        return False
    except Exception as e:
        print(str(e))
        return Response({"error": "Internal server error"}, 500)
    finally:
        conn.close()
    