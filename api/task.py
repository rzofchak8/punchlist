# task.py
from flask import Blueprint, request, jsonify
import sqlite3

task_bp = Blueprint('task', __name__)

DB_PATH = 'db.sqlite3'

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Task (task_list_id, room_id, task_type_id, description, status, location, due_date, priority)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['task_list_id'], data['room_id'], data.get('task_type_id'),
        data['description'], data['status'], data['location'], data['due_date'], data.get('priority')
    ))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return jsonify({"task_id": task_id}), 201

@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Task WHERE id = ?', (task_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        keys = [description[0] for description in cursor.description]
        return jsonify(dict(zip(keys, row)))
    return jsonify({"error": "Task not found"}), 404

@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Task SET description=?, status=?, location=?, due_date=?, priority=?, task_type_id=?
        WHERE id=?
    ''', (
        data['description'], data['status'], data['location'], data['due_date'], data.get('priority'), data.get('task_type_id'), task_id
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task updated"})

@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Task WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task deleted"})


# tasklist.py
from flask import Blueprint, request, jsonify
import sqlite3

tasklist_bp = Blueprint('tasklist', __name__)

DB_PATH = 'db.sqlite3'

@tasklist_bp.route('/tasklists', methods=['POST'])
def create_tasklist():
    data = request.get_json()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO TaskList (room_id, name, house_id, category_id)
        VALUES (?, ?, ?, ?)
    ''', (data['room_id'], data['name'], data['house_id'], data['category_id']))
    conn.commit()
    tasklist_id = cursor.lastrowid
    conn.close()
    return jsonify({"tasklist_id": tasklist_id}), 201

@tasklist_bp.route('/tasklists/<int:tasklist_id>', methods=['GET'])
def get_tasklist(tasklist_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM TaskList WHERE id = ?', (tasklist_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        keys = [description[0] for description in cursor.description]
        return jsonify(dict(zip(keys, row)))
    return jsonify({"error": "TaskList not found"}), 404

@tasklist_bp.route('/tasklists/<int:tasklist_id>', methods=['PUT'])
def update_tasklist(tasklist_id):
    data = request.get_json()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE TaskList SET name=?, room_id=?, house_id=?, category_id=?
        WHERE id=?
    ''', (data['name'], data['room_id'], data['house_id'], data['category_id'], tasklist_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "TaskList updated"})

@tasklist_bp.route('/tasklists/<int:tasklist_id>', methods=['DELETE'])
def delete_tasklist(tasklist_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM TaskList WHERE id = ?', (tasklist_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "TaskList deleted"})


# tasktype.py
from flask import Blueprint, request, jsonify
import sqlite3

tasktype_bp = Blueprint('tasktype', __name__)

DB_PATH = 'db.sqlite3'

@tasktype_bp.route('/tasktypes', methods=['POST'])
def create_tasktype():
    data = request.get_json()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO TaskType (name, description) VALUES (?, ?)', (data['name'], data.get('description')))
    conn.commit()
    tasktype_id = cursor.lastrowid
    conn.close()
    return jsonify({"tasktype_id": tasktype_id}), 201

@tasktype_bp.route('/tasktypes/<int:tasktype_id>', methods=['GET'])
def get_tasktype(tasktype_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM TaskType WHERE id = ?', (tasktype_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        keys = [description[0] for description in cursor.description]
        return jsonify(dict(zip(keys, row)))
    return jsonify({"error": "TaskType not found"}), 404

@tasktype_bp.route('/tasktypes/<int:tasktype_id>', methods=['PUT'])
def update_tasktype(tasktype_id):
    data = request.get_json()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE TaskType SET name=?, description=? WHERE id=?', (data['name'], data.get('description'), tasktype_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "TaskType updated"})

@tasktype_bp.route('/tasktypes/<int:tasktype_id>', methods=['DELETE'])
def delete_tasktype(tasktype_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM TaskType WHERE id = ?', (tasktype_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "TaskType deleted"})
