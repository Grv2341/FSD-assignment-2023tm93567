from models.response import Response
from models.book import Book
from db import get_db_connection
import uuid
import requests

genreList = ["FANTASY", "FICTION", "MYSTERY", "ROMANCE", "THRILLER"]
availabilityList = ["AVAILABLE", "NOT_AVAILABLE"]

get_user_url = "http://localhost:5000/user/"

def create_book(data):
    if not validateBookData(data):
        return Response({"message": "Invalid Data"}, 400)
    
    conn = get_db_connection()
    try:
        if check_duplicate_book(data):
            return Response({"message": "Duplicate Data"}, 400)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO books (id, title, author, genre, location, availability, userId) VALUES (?, ?, ?, ?, ?, ?, ?)',(str(uuid.uuid4()), data["title"], data["author"], data["genre"], data["location"], data["availability"], data["userId"]))
        conn.commit()
        payload = {
            "message": "Book Added Succesfully."
        }
        return Response(payload, 201)
    except Exception as e:
        print(str(e))
        return Response({"error": "Internal server error"}, 500)
    finally:
        conn.close()

def get_book_query(data):
    base_query = 'SELECT * FROM books WHERE 1=1'
    parameters = []
    page_offset = 0
    per_page = 10

    if "pageOffset" in data and data["pageOffset"] >= 0:
        page_offset = data["pageOffset"]

    if "perPage" in data and data["perPage"] >= 0:
        per_page = data["perPage"]

    starting_index = per_page * page_offset
    end_index = starting_index + per_page

    if "query" in data and len(data["query"].strip()) > 0:
        base_query += ' AND (title LIKE ? OR author LIKE ? OR location LIKE ?)'
        search_string = data["query"].strip()
        parameters.append(f"%{search_string}%")
        parameters.append(f"%{search_string}%")
        parameters.append(f"%{search_string}%")

    if "userId" in data and len(data["userId"].strip()) > 0:
        base_query += ' AND userId = ?'
        parameters.append(data["userId"])
    
    if "genre" in data and len(data["genre"].strip()) > 0:
        base_query += ' AND genre = ?'
        parameters.append(data["genre"])

    if "availability" in data and len(data["availability"].strip()) > 0:
        base_query += ' AND availability = ?'
        parameters.append(data["availability"])

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(base_query, parameters)
        books = cursor.fetchall()
        
        if starting_index >= len(books):
            return Response([], 200)

        result = []
        if end_index > len(books):
            end_index = len(books)
        for book in books:
            result.append(Book.from_row(book).to_json())

        return Response(result[starting_index:end_index], 200)
    except Exception as e:
        print(str(e))
        return Response({"error": "Internal server error"}, 500)
    finally:
        conn.close()

def get_book_id(bookId):
    if len(bookId.strip()) <=0:
        return Response({"message": "Invalid Data"}, 400)
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books WHERE id = ?', (bookId,))
        book = cursor.fetchone()
        if book:
            result = Book.from_row(book).to_json()
            userName = get_user_name(result["userId"])
            if userName == None:
                return Response({"error": "Internal server error"}, 500)
            result["userName"] = userName
            return Response(result, 200)
        return Response({"message": "Not Found"}, 404)
    except Exception as e:
        print(str(e))
        return Response({"error": "Internal server error"}, 500)
    finally:
        conn.close()
    
def validateBookData(data):
    if "title" not in data or len(data["title"].strip()) <= 0:
        print(1)
        return False
    if "author" not in data or len(data["author"].strip()) <= 0 or not all(part.isalpha() for part in data["author"].split()):
        print(len(data["author"].strip()))
        print(data["author"].strip().isalpha())
        print(data["author"].strip())
        return False
    if "genre" not in data or len(data["genre"].strip()) <= 0 or data["genre"] not in genreList:
        print(3)
        return False
    if "availability" not in data or len(data["availability"].strip()) <= 0 or data["availability"] not in availabilityList:
        print(4)
        return False
    if "location" not in data or len(data["location"].strip()) <= 0 or not all(part.isalpha() for part in data["location"].split()):
        print(5)
        return False
    if "userId" not in data or len(data["userId"].strip()) <= 0:
        print(6)
        return False
    return True

def check_duplicate_book(data):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books WHERE title = ? AND author = ? AND userId = ?', (data["title"],data["author"],data["userId"],))
        book = cursor.fetchone()
        if book:
            return True
        return False
    finally:
        conn.close()

def get_user_name(userId):
    url = get_user_url + userId

    try:
        response = requests.get(url)

        if response.status_code == 200:
            user = response.json()
            userName = user["firstName"] + " " + user["lastName"]
            return userName
        else:
            return None
    except Exception as e:
        print(str(e))
        return None