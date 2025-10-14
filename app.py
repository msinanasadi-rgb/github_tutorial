from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / 'app.db'

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


@app.route('/')
def index():
    conn = get_db_connection()
    try:
        rows = conn.execute("SELECT id, title, notes, created_at FROM items ORDER BY created_at DESC").fetchall()
        items = [dict(r) for r in rows]
    finally:
        conn.close()
    return render_template('index.html', items=items)


@app.route('/api/items', methods=['GET'])
def list_items():
    conn = get_db_connection()
    try:
        rows = conn.execute("SELECT id, title, notes, created_at FROM items ORDER BY created_at DESC").fetchall()
        items = [dict(r) for r in rows]
    finally:
        conn.close()
    return jsonify(items)


@app.route('/api/items', methods=['POST'])
def add_item():
    data = request.get_json(silent=True) or request.form
    title = (data.get('title') or '').strip()
    notes = (data.get('notes') or '').strip()
    if not title:
        return jsonify({"error": "title is required"}), 400
    conn = get_db_connection()
    try:
        cur = conn.execute("INSERT INTO items(title, notes) VALUES (?, ?)", (title, notes))
        conn.commit()
        item_id = cur.lastrowid
    finally:
        conn.close()
    if request.is_json:
        return jsonify({"id": item_id, "title": title, "notes": notes}), 201
    return redirect(url_for('index'))


@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id: int):
    conn = get_db_connection()
    try:
        cur = conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()
        deleted = cur.rowcount
    finally:
        conn.close()
    if deleted == 0:
        return jsonify({"error": "not found"}), 404
    return jsonify({"ok": True})


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
