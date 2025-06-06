from flask import request, jsonify
from db import get_db
from . import api_bp
import sqlite3
import hashlib

def hash_password(password):
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()

# User routes
@api_bp.route('/users', methods=['GET'])
def get_users():
    db = get_db()
    users = db.execute('SELECT id, name, email FROM user').fetchall()
    return jsonify([dict(user) for user in users])

@api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db = get_db()
    user = db.execute('SELECT id, name, email FROM user WHERE id = ?', (user_id,)).fetchone()
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(dict(user))

@api_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not all(k in data for k in ('name', 'email', 'password')):
        return jsonify({'error': 'Missing required fields'}), 400
    
    db = get_db()
    try:
        cursor = db.execute(
            'INSERT INTO user (name, email, password_hash) VALUES (?, ?, ?)',
            (data['name'], data['email'], hash_password(data['password']))
        )
        db.commit()
        return jsonify({'id': cursor.lastrowid, 'message': 'User created successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already exists'}), 400

@api_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    db = get_db()
    
    # Check if user exists
    user = db.execute('SELECT id FROM user WHERE id = ?', (user_id,)).fetchone()
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    
    # Build update query dynamically
    fields = []
    values = []
    if 'name' in data:
        fields.append('name = ?')
        values.append(data['name'])
    if 'email' in data:
        fields.append('email = ?')
        values.append(data['email'])
    if 'password' in data:
        fields.append('password_hash = ?')
        values.append(hash_password(data['password']))
    
    if not fields:
        return jsonify({'error': 'No valid fields to update'}), 400
    
    values.append(user_id)
    
    try:
        db.execute(f'UPDATE user SET {", ".join(fields)} WHERE id = ?', values)
        db.commit()
        return jsonify({'message': 'User updated successfully'})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already exists'}), 400

@api_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db = get_db()
    cursor = db.execute('DELETE FROM user WHERE id = ?', (user_id,))
    db.commit()
    
    if cursor.rowcount == 0:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'message': 'User deleted successfully'})
