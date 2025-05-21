from flask import Blueprint, request, jsonify
from sqlite3 import IntegrityError

user_bp = Blueprint('user', __name__)

def get_db():
    from app import get_db
    return get_db()

@user_bp.route('/api/users', methods=['GET'])
def get_all_users():
    db = get_db()
    users = db.execute('SELECT * FROM user').fetchall()
    return jsonify([dict(u) for u in users])

@user_bp.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db = get_db()
    user = db.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
    if user:
        return jsonify(dict(user))
    return jsonify({'error': 'User not found'}), 404

@user_bp.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        db = get_db()
        cursor = db.execute(
            'INSERT INTO user (name, email) VALUES (?, ?)',
            (data['name'], data['email'])
        )
        db.commit()
        return jsonify({'id': cursor.lastrowid}), 201
    except IntegrityError as e:
        return jsonify({'error': str(e)}), 400

@user_bp.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    db = get_db()
    db.execute(
        'UPDATE user SET name = ?, email = ? WHERE id = ?',
        (data['name'], data['email'], user_id)
    )
    db.commit()
    return jsonify({'message': 'User updated'})

@user_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db = get_db()
    db.execute('DELETE FROM user WHERE id = ?', (user_id,))
    db.commit()
    return jsonify({'message': 'User deleted'})
