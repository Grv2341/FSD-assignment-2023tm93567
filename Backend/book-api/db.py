import sqlite3

DATABASE = 'database.db'

def get_db_connection():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                genre TEXT NOT NULL,
                location TEXT NOT NULL,
                availability TEXT NOT NULL,
                userId TEXT NOT NULL
            )
        ''')