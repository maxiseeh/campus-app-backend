import psycopg2
import psycopg2.extras
import os
import bcrypt


def get_db():
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not configured")
    return psycopg2.connect(url)


def create_user(name: str, email: str, password: str) -> dict | None:
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("SELECT id FROM users WHERE email = %s", (email,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return None

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    cur.execute(
        "INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING id, name, email",
        (name, email, password_hash),
    )
    user = dict(cur.fetchone())
    conn.commit()
    cur.close()
    conn.close()
    return {"id": user["id"], "username": user["name"], "email": user["email"]}


def authenticate_user(email: str, password: str) -> dict | None:
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user:
        return None

    stored = user["password"]
    try:
        match = bcrypt.checkpw(password.encode("utf-8"), stored.encode("utf-8"))
    except Exception:
        return None

    if not match:
        return None

    return {"id": user["id"], "username": user["name"], "email": user["email"]}


def get_user_by_id(user_id: int) -> dict | None:
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT id, name, email FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return {"id": user["id"], "username": user["name"], "email": user["email"]} if user else None