from flask import Blueprint, request, jsonify, current_app
import os
import uuid

photo_bp = Blueprint('photo', __name__)

def get_db():
    from app import get_db
    return get_db()

@photo_bp.route('/api/photos', methods=['GET'])
def get_all_photos():
    db = get_db()
    photos = db.execute('SELECT * FROM photo').fetchall()
    return jsonify([dict(p) for p in photos])

@photo_bp.route('/api/photos/<int:photo_id>', methods=['GET'])
def get_photo(photo_id):
    db = get_db()
    photo = db.execute('SELECT * FROM photo WHERE id = ?', (photo_id,)).fetchone()
    if photo:
        return jsonify(dict(photo))
    return jsonify({'error': 'Photo not found'}), 404

@photo_bp.route('/api/photos', methods=['POST'])
def upload_photo():
    file = request.files.get('file')
    room_id = request.form.get('room_id')
    if not file or not room_id:
        return jsonify({'error': 'Missing file or room_id'}), 400

    filename = f"{uuid.uuid4().hex}_{file.filename}"
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Optionally invoke image processing pipeline here

    db = get_db()
    cursor = db.execute(
        'INSERT INTO photo (room_id, path, description) VALUES (?, ?, ?)',
        (room_id, filename, request.form.get('description'))
    )
    db.commit()
    return jsonify({'id': cursor.lastrowid, 'path': filename}), 201

@photo_bp.route('/api/photos/<int:photo_id>', methods=['DELETE'])
def delete_photo(photo_id):
    db = get_db()
    photo = db.execute('SELECT * FROM photo WHERE id = ?', (photo_id,)).fetchone()
    if not photo:
        return jsonify({'error': 'Photo not found'}), 404
    try:
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], photo['path']))
    except FileNotFoundError:
        pass
    db.execute('DELETE FROM photo WHERE id = ?', (photo_id,))
    db.commit()
    return jsonify({'message': 'Photo deleted'})
