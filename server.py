from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# --- Config ---
DATABASE = 'task_server.db'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, DATABASE)

# --- Database Helpers ---
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# --- Initialization ---
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# --- Routes ---
@app.route('/')
def index():
    db = get_db()
    houses = db.execute('SELECT * FROM house').fetchall()
    return render_template('index.html', houses=houses)

@app.route('/house/<int:house_id>/rooms')
def view_rooms(house_id):
    db = get_db()
    house = db.execute('SELECT * FROM house WHERE id = ?', (house_id,)).fetchone()
    rooms = db.execute('SELECT * FROM room WHERE house_id = ?', (house_id,)).fetchall()
    return render_template('rooms.html', house=house, rooms=rooms)

@app.route('/room/<int:room_id>/tasks')
def room_tasks(room_id):
    db = get_db()
    room = db.execute('SELECT * FROM room WHERE id = ?', (room_id,)).fetchone()
    tasklists = db.execute('SELECT * FROM tasklist WHERE room_id = ?', (room_id,)).fetchall()
    categories = db.execute('SELECT * FROM taskcategory').fetchall()
    tasks = db.execute('SELECT * FROM task WHERE room_id = ?', (room_id,)).fetchall()
    return render_template('tasks.html', room=room, tasklists=tasklists, categories=categories, tasks=tasks)

@app.route('/room/<int:room_id>/task', methods=['POST'])
def add_task(room_id):
    db = get_db()
    description = request.form['description']
    category_id = request.form['category_id']
    db.execute(
        'INSERT INTO task (room_id, category_id, description, status, created_at) VALUES (?, ?, ?, ?, ?)',
        (room_id, category_id, description, 'pending', datetime.utcnow())
    )
    db.commit()
    return redirect(url_for('room_tasks', room_id=room_id))

# --- CLI Commands ---
@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')

# --- Main Entry ---
if __name__ == '__main__':
    app.run(debug=True)
