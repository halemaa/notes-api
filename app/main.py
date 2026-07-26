import os

import psycopg2
from flask import Flask, jsonify, request
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "database": os.getenv("DB_NAME", "notes"),
    "user": os.getenv("DB_USER", "notes_user"),
    "password": os.getenv("DB_PASSWORD", "changeme"),
}


def get_conn():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)


@app.route("/health")
def health():
    return {"status": "ok"}, 200


@app.route("/notes", methods=["GET"])
def list_notes():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT id, title, body, created_at FROM notes ORDER BY id DESC;")
        return jsonify(cur.fetchall())


@app.route("/notes", methods=["POST"])
def create_note():
    data = request.get_json() or {}
    title = data.get("title")
    body = data.get("body", "")
    if not title:
        return {"error": "title is required"}, 400

    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO notes (title, body) VALUES (%s, %s) RETURNING id;",
            (title, body),
        )
        note_id = cur.fetchone()["id"]
        conn.commit()
        return {"id": note_id, "title": title, "body": body}, 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
