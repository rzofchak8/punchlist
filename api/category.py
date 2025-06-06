from flask import request, jsonify
from db import get_db
from . import api_bp

# Category routes
@api_bp.route('/categories', methods=['GET'])
def get_categories():
    db = get_db()
    categories = db.execute('SELECT * FROM category').fetchall()
    return jsonify([dict(category) for category in categories])

@api_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    db = get_db()
    category = db.execute('SELECT * FROM category WHERE id = ?', (category_id,)).fetchone()
    if category is None:
        return jsonify({'error': 'Category not found'}), 404
    return jsonify(dict(category))

@api_bp.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    db = get_db()
    cursor = db.execute(
        'INSERT INTO category (name, symbolMeta) VALUES (?, ?)',
        (data['name'], data.get('symbolMeta'))
    )
    db.commit()
    return jsonify({'id': cursor.lastrowid, 'message': 'Category created successfully'}), 201

@api_bp.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    db = get_db()
    
    # Check if category exists
    category = db.execute('SELECT id FROM category WHERE id = ?', (category_id,)).fetchone()
    if category is None:
        return jsonify({'error': 'Category not found'}), 404
    
    # Build update query
    fields = []
    values = []
    for field in ['name', 'symbolMeta']:
        if field in data:
            fields.append(f'{field} = ?')
            values.append(data[field])
    
    if not fields:
        return jsonify({'error': 'No valid fields to update'}), 400
    
    values.append(category_id)
    db.execute(f'UPDATE category SET {", ".join(fields)} WHERE id = ?', values)
    db.commit()
    return jsonify({'message': 'Category updated successfully'})

@api_bp.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    db = get_db()
    cursor = db.execute('DELETE FROM category WHERE id = ?', (category_id,))
    db.commit()
    
    if cursor.rowcount == 0:
        return jsonify({'error': 'Category not found'}), 404
    return jsonify({'message': 'Category deleted successfully'})
