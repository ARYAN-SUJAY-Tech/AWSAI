import sqlite3

DB_NAME = "app.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        username TEXT,
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


def create_user(email, username, password):
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()

    # Check if user already exists
    cur.execute("SELECT 1 FROM users WHERE email = ?", (email,))
    if cur.fetchone():
        conn.close()
        return "exists"

    # Insert new user
    cur.execute(
        "INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
        (email, username, password)
    )
    conn.commit()
    conn.close()
    return "created"




def authenticate_user(email, password):
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()
    cur.execute(
        "SELECT username FROM users WHERE email=? AND password=?",
        (email, password)
    )
    user = cur.fetchone()
    conn.close()
    return user  # returns (username,) or None



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

def reset_password(email, new_password):
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()
    cur.execute("SELECT email FROM users WHERE email=?", (email,))
    if not cur.fetchone():
        conn.close()
        return False

    cur.execute("UPDATE users SET password=? WHERE email=?", (new_password, email))
    conn.commit()
    conn.close()
    return True

