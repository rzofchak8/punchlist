from flask import request, jsonify
from db import get_db
from . import api_bp

# Photo routes
@api_bp.route('/photos', methods=['GET'])
def get_photos():
    room_id = request.args.get('room_id')
    db = get_db()
    
    if room_id:
        photos = db.execute('SELECT * FROM photo WHERE room_id = ?', (room_id,)).fetchall()
    else:
        photos = db.execute('SELECT * FROM photo').fetchall()
    
    return jsonify([dict(photo) for photo in photos])

@api_bp.route('/photos/<int:photo_id>', methods=['GET'])
def get_photo(photo_id):
    db = get_db()
    photo = db.execute('SELECT * FROM photo WHERE id = ?', (photo_id,)).fetchone()
    if photo is None:
        return jsonify({'error': 'Photo not found'}), 404
    return jsonify(dict(photo))

@api_bp.route('/photos', methods=['POST'])
def create_photo():
    data = request.get_json()
    if not data or not all(k in data for k in ('room_id', 'path')):
        return jsonify({'error': 'room_id and path are required'}), 400
    
    db = get_db()
    cursor = db.execute(
        'INSERT INTO photo (room_id, path) VALUES (?, ?)',
        (data['room_id'], data['path'])
    )
    db.commit()
    return jsonify({'id': cursor.lastrowid, 'message': 'Photo created successfully'}), 201

@api_bp.route('/photos/<int:photo_id>', methods=['PUT'])
def update_photo(photo_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    db = get_db()
    
    # Check if photo exists
    photo = db.execute('SELECT id FROM photo WHERE id = ?', (photo_id,)).fetchone()
    if photo is None:
        return jsonify({'error': 'Photo not found'}), 404
    
    # Build update query
    fields = []
    values = []
    for field in ['room_id', 'path']:
        if field in data:
            fields.append(f'{field} = ?')
            values.append(data[field])
    
    if not fields:
        return jsonify({'error': 'No valid fields to update'}), 400
    
    values.append(photo_id)
    db.execute(f'UPDATE photo SET {", ".join(fields)} WHERE id = ?', values)
    db.commit()
    return jsonify({'message': 'Photo updated successfully'})

@api_bp.route('/photos/<int:photo_id>', methods=['DELETE'])
def delete_photo(photo_id):
    db = get_db()
    cursor = db.execute('DELETE FROM photo WHERE id = ?', (photo_id,))
    db.commit()
    
    if cursor.rowcount == 0:
        return jsonify({'error': 'Photo not found'}), 404
    return jsonify({'message': 'Photo deleted successfully'})

