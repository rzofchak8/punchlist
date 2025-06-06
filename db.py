from flask import current_app, g
import sqlite3
import os

def get_db():
    """Get database connection - shared across all modules"""
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Initialize the database from schema.sql file if it doesn't exist yet"""
    db_path = current_app.config['DATABASE']

    if not os.path.exists(db_path):
        db = get_db()

        with current_app.open_resource('schema.sql') as f:
            db.executescript(f.read().decode('utf8'))

        db.commit()

def init_app(app):
    """Register database functions with the Flask app"""
    app.teardown_appcontext(close_db)