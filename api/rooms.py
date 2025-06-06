from flask import request, jsonify
from db import get_db
import sqlite3
from . import api_bp

# Room routes
@api_bp.route('/rooms', methods=['GET'])
def get_rooms():
    house_id = request.args.get('house_id')
    db = get_db()
    
    if house_id:
        rooms = db.execute('SELECT * FROM room WHERE house_id = ?', (house_id,)).fetchall()
    else:
        rooms = db.execute('SELECT * FROM room').fetchall()
    
    return jsonify([dict(room) for room in rooms])

@api_bp.route('/rooms/<int:room_id>', methods=['GET'])
def get_room(room_id):
    db = get_db()
    room = db.execute('SELECT * FROM room WHERE id = ?', (room_id,)).fetchone()
    if room is None:
        return jsonify({'error': 'Room not found'}), 404
    return jsonify(dict(room))

@api_bp.route('/rooms', methods=['POST'])
def create_room():
    data = request.get_json()
    if not data or not all(k in data for k in ('house_id', 'name')):
        return jsonify({'error': 'house_id and name are required'}), 400
    
    db = get_db()
    try:
        cursor = db.execute(
            'INSERT INTO room (house_id, name, description) VALUES (?, ?, ?)',
            (data['house_id'], data['name'], data.get('description'))
        )
        db.commit()
        return jsonify({'id': cursor.lastrowid, 'message': 'Room created successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Room name must be unique or house does not exist'}), 400

@api_bp.route('/rooms/<int:room_id>', methods=['PUT'])
def update_room(room_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    db = get_db()
    
    # Check if room exists
    room = db.execute('SELECT id FROM room WHERE id = ?', (room_id,)).fetchone()
    if room is None:
        return jsonify({'error': 'Room not found'}), 404
    
    # Build update query
    fields = []
    values = []
    for field in ['house_id', 'name', 'description']:
        if field in data:
            fields.append(f'{field} = ?')
            values.append(data[field])
    
    if not fields:
        return jsonify({'error': 'No valid fields to update'}), 400
    
    values.append(room_id)
    
    try:
        db.execute(f'UPDATE room SET {", ".join(fields)} WHERE id = ?', values)
        db.commit()
        return jsonify({'message': 'Room updated successfully'})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Room name must be unique or house does not exist'}), 400

@api_bp.route('/rooms/<int:room_id>', methods=['DELETE'])
def delete_room(room_id):
    db = get_db()
    cursor = db.execute('DELETE FROM room WHERE id = ?', (room_id,))
    db.commit()
    
    if cursor.rowcount == 0:
        return jsonify({'error': 'Room not found'}), 404
    return jsonify({'message': 'Room deleted successfully'})

