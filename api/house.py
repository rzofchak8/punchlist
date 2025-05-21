from flask import Blueprint, request, jsonify, g
from sqlite3 import IntegrityError

house_bp = Blueprint('house', __name__)

def get_db():
    from app import get_db  # Import from main app context
    return get_db()

@house_bp.route('/api/houses', methods=['GET'])
def get_all_houses():
    db = get_db()
    houses = db.execute('SELECT * FROM house').fetchall()
    return jsonify([dict(h) for h in houses])

@house_bp.route('/api/houses/<int:house_id>', methods=['GET'])
def get_house(house_id):
    db = get_db()
    house = db.execute('SELECT * FROM house WHERE id = ?', (house_id,)).fetchone()
    if house:
        return jsonify(dict(house))
    return jsonify({'error': 'House not found'}), 404

@house_bp.route('/api/houses', methods=['POST'])
def create_house():
    data = request.get_json()
    try:
        db = get_db()
        cursor = db.execute(
            'INSERT INTO house (name, address, is_complete, note) VALUES (?, ?, ?, ?)',
            (data['name'], data.get('address'), data.get('is_complete', False), data.get('note'))
        )
        db.commit()
        return jsonify({'id': cursor.lastrowid}), 201
    except IntegrityError as e:
        return jsonify({'error': str(e)}), 400

@house_bp.route('/api/houses/<int:house_id>', methods=['PUT'])
def update_house(house_id):
    data = request.get_json()
    db = get_db()
    db.execute(
        'UPDATE house SET name = ?, address = ?, is_complete = ?, note = ? WHERE id = ?',
        (data['name'], data.get('address'), data.get('is_complete', False), data.get('note'), house_id)
    )
    db.commit()
    return jsonify({'message': 'House updated'})

@house_bp.route('/api/houses/<int:house_id>', methods=['DELETE'])
def delete_house(house_id):
    db = get_db()
    db.execute('DELETE FROM house WHERE id = ?', (house_id,))
    db.commit()
    return jsonify({'message': 'House deleted'})
