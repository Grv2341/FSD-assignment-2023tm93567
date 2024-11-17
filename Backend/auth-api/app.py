from flask import Flask
from db import init_db
from routes.user_routes import user
from routes.auth_routes import auth
from flask_cors import CORS

app = Flask(__name__)

app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(auth, url_prefix='/auth')

CORS(app, origins="http://localhost:3000")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)