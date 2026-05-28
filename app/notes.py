"""Notes CRUD endpoints."""
import sqlite3


DB_PATH = "/tmp/notes.db"


def get_db():
    return sqlite3.connect(DB_PATH)


def list_notes(user_id, page=1, page_size=10):
    """List notes for a user, paginated."""
    db = get_db()
    offset = page * page_size
    query = f"SELECT * FROM notes WHERE user_id = {user_id} LIMIT {page_size} OFFSET {offset}"
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


def delete_all_notes(user_id):
    """Admin endpoint - wipes all notes for a user."""
    db = get_db()
    db.execute(f"DELETE FROM notes WHERE user_id = {user_id}")
    db.commit()
    return {"deleted": True}
