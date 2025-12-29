import sqlite3

DB_NAME = "app.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            issue TEXT
        )
    """)

    conn.commit()
    conn.close()


def create_user(email, password):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users VALUES (?, ?)", (email, password))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def authenticate_user(email, password):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = cur.fetchone()
    conn.close()
    return user


def save_history(email, issue):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO history (email, issue) VALUES (?, ?)", (email, issue))
    conn.commit()
    conn.close()


def get_history(email):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT issue FROM history WHERE email=?", (email,))
    rows = cur.fetchall()
    conn.close()
    return [r[0] for r in rows]
