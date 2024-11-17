from models.response import Response
from db import get_db_connection
from werkzeug.security import check_password_hash
from datetime import datetime
import uuid

def authenticate_user(data):
    if not validateUserData(data):
        return Response({"error": "Imvalid Data"}, 400)

    conn = get_db_connection()

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (data["email"],))
        user = cursor.fetchone()
        print(user)
        if user and check_password_hash(user[2], data["password"]):
            sessionId = create_session(user[0])
            payload = {
                "message": "User authenticated",
                "sessionId": sessionId,
                "userId": user[0]
            }
            return Response(payload, 200)
        else:
            return Response({"error": "Authentication Failed"}, 403)
    except Exception as e:
        print(str(e))
        return Response({"error": "Internal server error"}, 500)
    finally:
        conn.close()

def authenticate_session(data):
    if "sessionId" not in data or len(data["sessionId"].strip()) <= 0:
        return Response({"error": "Imvalid Data"}, 400)

    conn = get_db_connection()

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sessions WHERE id = ?', (data["sessionId"],))
        session = cursor.fetchone()

        if session:
            if session[2] > datetime.now().timestamp():
                return Response({"message": "Session authenticated"}, 200)
            delete_session_userId(session[1])
        return Response({"message": "Invalid session"}, 403)
    except Exception as e:
        print(str(e))
        return Response({"error": "Internal server error"}, 500)
    finally:
        conn.close()   
        
def validateUserData(data):
    if "email" not in data or len(data["email"].strip()) <= 0:
        return False
    if "password" not in data or len(data["password"].strip()) <= 0:
        return False
    return True

def create_session(userId):
    conn = get_db_connection()

    try:
        delete_session_userId(userId)
        cursor = conn.cursor()

        ttl = datetime.now().timestamp() + 300
        sessionId = str(uuid.uuid4())

        cursor.execute('INSERT INTO sessions (id, userId, ttl) VALUES (?, ?, ?)',(sessionId, userId, ttl))
        conn.commit()
        return sessionId
    finally:
        conn.close()

def delete_session_userId(userId):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM sessions WHERE userId = ?', (userId,))
        conn.commit()
    finally:
        conn.close()
