import sqlite3
import os
from dotenv import load_dotenv


load_dotenv()

def get_connection():
    db=os.environ.get("DATABASE","todos.db")
    conn= sqlite3.connect(db)
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    conn=get_connection()
    conn.execute("""
     CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        done BOOLEAN NOT NULL DEFAULT 0,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES useres(id) 
    )
    """)
    conn.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )""")
    conn.commit()
    conn.close()


