# modules/db_module.py
import sqlite3
from datetime import datetime

DB_FILE = "interaction.db"

def create_table():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT NOT NULL,
            ai_reply TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_interaction(user_input: str, ai_reply: str):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO interactions (user_input, ai_reply, timestamp)
        VALUES (?, ?, ?)
    """, (user_input, ai_reply, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def fetch_all_interactions():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, user_input, ai_reply, timestamp FROM interactions ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "user_input": r[1], "ai_reply": r[2], "timestamp": r[3]} for r in rows]

# ensure DB is initialized on import
create_table()
