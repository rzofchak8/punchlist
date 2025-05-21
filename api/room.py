from flask import Blueprint, request, jsonify
from sqlite3 import IntegrityError

room_bp = Blueprint('room', __name__)

def get_db():
    from app import get_db
    return get_db()

@room_bp.route('/api/rooms', methods=['GET'])
def get_all_rooms():
    db = get_db()
    rooms = db.execute('SELECT * FROM room').fetchall()
    return jsonify([dict(r) for r in rooms])

@room_bp.route('/api/rooms/<int:room_id>', methods=['GET'])
def get_room(room_id):
    db = get_db()
    room = db.execute('SELECT * FROM room WHERE id = ?', (room_id,)).fetchone()
    if room:
        return jsonify(dict(room))
    return jsonify({'error': 'Room not found'}), 404

@room_bp.route('/api/rooms', methods=['POST'])
def create_room():
    data = request.get_json()
    try:
        db = get_db()
        cursor = db.execute(
            'INSERT INTO room (house_id, name, description) VALUES (?, ?, ?)',
            (data['house_id'], data['name'], data.get('description'))
        )
        db.commit()
        return jsonify({'id': cursor.lastrowid}), 201
    except IntegrityError as e:
        return jsonify({'error': str(e)}), 400

@room_bp.route('/api/rooms/<int:room_id>', methods=['PUT'])
def update_room(room_id):
    data = request.get_json()
    db = get_db()
    db.execute(
        'UPDATE room SET house_id = ?, name = ?, description = ? WHERE id = ?',
        (data['house_id'], data['name'], data.get('description'), room_id)
    )
    db.commit()
    return jsonify({'message': 'Room updated'})

@room_bp.route('/api/rooms/<int:room_id>', methods=['DELETE'])
def delete_room(room_id):
    db = get_db()
    db.execute('DELETE FROM room WHERE id = ?', (room_id,))
    db.commit()
    return jsonify({'message': 'Room deleted'})
