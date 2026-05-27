import psycopg2
import psycopg2.extras
import os


def get_db():
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not configured")
    return psycopg2.connect(url)


def serialize_post(post: dict) -> dict:
    event_date = post.get("event_date")
    created_at = post.get("created_at")
    return {
        "id": post["id"],
        "title": post["title"],
        "description": post.get("body"),
        "category": (post.get("category") or "").replace("-", "_"),
        "authorName": post.get("username") or "Unknown",
        "contactInfo": post.get("contact_info"),
        "location": post.get("location"),
        "eventDate": event_date.isoformat() if event_date else None,
        "createdAt": created_at.isoformat() if created_at else None,
        "userId": post["author_id"],
    }


def fetch_post_stats() -> dict:
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT category, COUNT(*)::int AS count FROM posts GROUP BY category")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    counts: dict[str, int] = {}
    total = 0
    for row in rows:
        cat = (row["category"] or "").replace("-", "_")
        counts[cat] = row["count"]
        total += row["count"]

    return {
        "total": total,
        "studyGroups": counts.get("study_group", 0),
        "events": counts.get("event", 0),
        "lostFound": counts.get("lost_found", 0),
        "announcements": counts.get("announcement", 0),
    }


def fetch_recent_posts(limit: int = 5) -> list[dict]:
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        """
        SELECT p.*, u.name AS username
        FROM posts p
        LEFT JOIN users u ON u.id = p.author_id
        ORDER BY p.created_at DESC
        LIMIT %s
        """,
        (limit,),
    )
    posts = cur.fetchall()
    cur.close()
    conn.close()
    return [serialize_post(dict(p)) for p in posts]


def fetch_all_posts(category: str | None = None, search: str | None = None) -> list[dict]:
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    if category:
        category_hyphen = category.replace("_", "-")
        cur.execute(
            """
            SELECT p.*, u.name AS username
            FROM posts p
            LEFT JOIN users u ON u.id = p.author_id
            WHERE p.category = %s OR p.category = %s
            ORDER BY p.created_at DESC
            """,
            (category, category_hyphen),
        )
    else:
        cur.execute(
            """
            SELECT p.*, u.name AS username
            FROM posts p
            LEFT JOIN users u ON u.id = p.author_id
            ORDER BY p.created_at DESC
            """
        )

    posts = [dict(p) for p in cur.fetchall()]
    cur.close()
    conn.close()

    if search:
        term = search.lower()
        posts = [
            p for p in posts
            if term in (p.get("title") or "").lower()
            or term in (p.get("body") or "").lower()
            or term in (p.get("name") or "").lower()
        ]

    return [serialize_post(p) for p in posts]


def fetch_post_by_id(post_id: int) -> dict | None:
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        """
        SELECT p.*, u.name AS username
        FROM posts p
        LEFT JOIN users u ON u.id = p.author_id
        WHERE p.id = %s
        """,
        (post_id,),
    )
    post = cur.fetchone()
    cur.close()
    conn.close()
    return serialize_post(dict(post)) if post else None


def insert_post(user_id: int, username: str, data: dict) -> dict:
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    event_date = data.get("eventDate") or None

    cur.execute(
        """
        INSERT INTO posts (title, body, category, author_id, contact_info, location, event_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING *
        """,
        (
            data["title"],
            data.get("description") or "",
            data["category"],
            user_id,
            data.get("contactInfo") or None,
            data.get("location") or None,
            event_date,
        ),
    )
    post = dict(cur.fetchone())
    conn.commit()
    cur.close()
    conn.close()
    post["username"] = username
    return serialize_post(post)


def remove_post(post_id: int) -> dict | None:
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT author_id FROM posts WHERE id = %s", (post_id,))
    post = cur.fetchone()
    if not post:
        cur.close()
        conn.close()
        return None
    cur.execute("DELETE FROM posts WHERE id = %s", (post_id,))
    conn.commit()
    cur.close()
    conn.close()
    return dict(post)