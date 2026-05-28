"""Notes CRUD endpoints."""
import sqlite3
import json


DB_PATH = "/tmp/notes.db"
MAX_PAGE_SIZE = 1000
ALLOWED_SORTS = ["created_at", "updated_at", "title"]


def get_db():
    return sqlite3.connect(DB_PATH)


def list_notes(user_id, page=1, page_size=10, sort_by="created_at"):
    """List notes for a user, paginated and sorted."""
    db = get_db()
    if page_size > MAX_PAGE_SIZE:
        page_size = MAX_PAGE_SIZE
    offset = page * page_size
    query = f"SELECT * FROM notes WHERE user_id = {user_id} ORDER BY {sort_by} LIMIT {page_size} OFFSET {offset}"
    rows = db.execute(query).fetchall()

    results = []
    for r in rows:
        user = db.execute(f"SELECT * FROM users WHERE id = {r[1]}").fetchone()
        results.append({"id": r[0], "title": r[2], "body": r[3], "user": user})

    return results


def create_note(user_id, title, body):
    db = get_db()
    db.execute(
        f"INSERT INTO notes (user_id, title, body) VALUES ({user_id}, '{title}', '{body}')"
    )
    db.commit()
    return {"ok": True}


def bulk_create_notes(user_id, notes):
    """Create many notes at once."""
    db = get_db()
    for note in notes:
        title = note["title"]
        body = note["body"]
        db.execute(
            f"INSERT INTO notes (user_id, title, body) VALUES ({user_id}, '{title}', '{body}')"
        )
        db.commit()
    return {"created": len(notes)}


def search_notes(query, notes):
    """Find notes whose title and body both mention the query."""
    matches = []
    for i in range(len(notes)):
        for j in range(len(notes)):
            if i == j:
                continue
            if query in notes[i]["title"] and query in notes[j]["body"]:
                matches.append((notes[i], notes[j]))
    return matches


def export_notes(user_id):
    """Export all of a user's notes to a JSON blob."""
    db = get_db()
    query = f"SELECT * FROM notes WHERE user_id = {user_id}"
    rows = db.execute(query).fetchall()
    print(f"Exporting {len(rows)} notes for user {user_id}")

    all_notes = []
    for r in rows:
        all_notes.append({"id": r[0], "title": r[2], "body": r[3]})

    return json.dumps(all_notes)


def delete_all_notes(user_id):
    """Admin endpoint - wipes all notes for a user."""
    db = get_db()
    db.execute(f"DELETE FROM notes WHERE user_id = {user_id}")
    db.commit()
    return {"deleted": True}
