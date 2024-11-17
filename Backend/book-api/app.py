from flask import Flask
from db import init_db
from routes.book_routes import book
from flask_cors import CORS

app = Flask(__name__)

CORS(app, origins="http://localhost:3000")

app.register_blueprint(book, url_prefix='/book')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='127.0.0.1', port=8080)