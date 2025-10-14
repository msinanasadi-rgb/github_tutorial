# Simple Store Website

A minimal Flask + SQLite app to store simple items with a title and optional notes. Includes a basic UI to add and delete items.

## Prerequisites
- Python 3.8+
- pip

## Setup
```bash
pip3 install -r requirements.txt
```

## Run
```bash
python3 app.py
```
The app starts on http://localhost:5000

## Endpoints
- `GET /` – Render UI
- `GET /api/items` – List items (JSON)
- `POST /api/items` – Create item via JSON or form
  - JSON: `{ "title": "...", "notes": "..." }`
  - Form: fields `title`, `notes`
- `DELETE /api/items/:id` – Delete item

## Database
SQLite file `app.db` created in the project folder on first run.
