from flask import request, jsonify
from db import get_db
from . import api_bp

# House routes
@api_bp.route('/houses', methods=['GET'])
def get_houses():
    db = get_db()
    houses = db.execute('SELECT * FROM house').fetchall()
    return jsonify([dict(house) for house in houses])

@api_bp.route('/houses/<int:house_id>', methods=['GET'])
def get_house(house_id):
    db = get_db()
    house = db.execute('SELECT * FROM house WHERE id = ?', (house_id,)).fetchone()
    if house is None:
        return jsonify({'error': 'House not found'}), 404
    return jsonify(dict(house))

@api_bp.route('/houses', methods=['POST'])
def create_house():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    db = get_db()
    cursor = db.execute(
        'INSERT INTO house (name, address, is_complete, note) VALUES (?, ?, ?, ?)',
        (data['name'], data.get('address'), data.get('is_complete', 0), data.get('note'))
    )
    db.commit()
    return jsonify({'id': cursor.lastrowid, 'message': 'House created successfully'}), 201

@api_bp.route('/houses/<int:house_id>', methods=['PUT'])
def update_house(house_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    db = get_db()
    
    # Check if house exists
    house = db.execute('SELECT id FROM house WHERE id = ?', (house_id,)).fetchone()
    if house is None:
        return jsonify({'error': 'House not found'}), 404
    
    # Build update query
    fields = []
    values = []
    for field in ['name', 'address', 'is_complete', 'note']:
        if field in data:
            fields.append(f'{field} = ?')
            values.append(data[field])
    
    if not fields:
        return jsonify({'error': 'No valid fields to update'}), 400
    
    values.append(house_id)
    db.execute(f'UPDATE house SET {", ".join(fields)} WHERE id = ?', values)
    db.commit()
    return jsonify({'message': 'House updated successfully'})

@api_bp.route('/houses/<int:house_id>', methods=['DELETE'])
def delete_house(house_id):
    db = get_db()
    cursor = db.execute('DELETE FROM house WHERE id = ?', (house_id,))
    db.commit()
    
    if cursor.rowcount == 0:
        return jsonify({'error': 'House not found'}), 404
    return jsonify({'message': 'House deleted successfully'})
