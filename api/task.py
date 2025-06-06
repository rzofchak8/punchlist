from flask import request, jsonify
from db import get_db
from . import api_bp

# Task routes
@api_bp.route('/tasks', methods=['GET'])
def get_tasks():
    room_id = request.args.get('room_id')
    category_id = request.args.get('category_id')
    status = request.args.get('status')
    
    db = get_db()
    query = 'SELECT * FROM task WHERE 1=1'
    params = []
    
    if room_id:
        query += ' AND room_id = ?'
        params.append(room_id)
    if category_id:
        query += ' AND category_id = ?'
        params.append(category_id)
    if status:
        query += ' AND status = ?'
        params.append(status)
    
    tasks = db.execute(query, params).fetchall()
    return jsonify([dict(task) for task in tasks])

@api_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    db = get_db()
    task = db.execute('SELECT * FROM task WHERE id = ?', (task_id,)).fetchone()
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(dict(task))

@api_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or not all(k in data for k in ('room_id', 'category_id', 'name')):
        return jsonify({'error': 'room_id, category_id, and name are required'}), 400
    
    db = get_db()
    cursor = db.execute(
        'INSERT INTO task (room_id, category_id, name, status, priority, type_id) VALUES (?, ?, ?, ?, ?, ?)',
        (data['room_id'], data['category_id'], data['name'], 
         data.get('status', 'pending'), data.get('priority', 0), data.get('type_id'))
    )
    db.commit()
    return jsonify({'id': cursor.lastrowid, 'message': 'Task created successfully'}), 201

@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    db = get_db()
    
    # Check if task exists
    task = db.execute('SELECT id FROM task WHERE id = ?', (task_id,)).fetchone()
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    
    # Build update query
    fields = []
    values = []
    for field in ['room_id', 'category_id', 'name', 'status', 'priority', 'type_id']:
        if field in data:
            fields.append(f'{field} = ?')
            values.append(data[field])
    
    if not fields:
        return jsonify({'error': 'No valid fields to update'}), 400
    
    values.append(task_id)
    db.execute(f'UPDATE task SET {", ".join(fields)} WHERE id = ?', values)
    db.commit()
    return jsonify({'message': 'Task updated successfully'})

@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    db = get_db()
    cursor = db.execute('DELETE FROM task WHERE id = ?', (task_id,))
    db.commit()
    
    if cursor.rowcount == 0:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'message': 'Task deleted successfully'})

# TaskType routes
@api_bp.route('/task-types', methods=['GET'])
def get_task_types():
    db = get_db()
    task_types = db.execute('SELECT * FROM taskType').fetchall()
    return jsonify([dict(task_type) for task_type in task_types])

@api_bp.route('/task-types', methods=['POST'])
def create_task_type():
    data = request.get_json()
    if not data or 'type' not in data:
        return jsonify({'error': 'Type is required'}), 400
    
    db = get_db()
    cursor = db.execute('INSERT INTO taskType (type) VALUES (?)', (data['type'],))
    db.commit()
    return jsonify({'id': cursor.lastrowid, 'message': 'Task type created successfully'}), 201
