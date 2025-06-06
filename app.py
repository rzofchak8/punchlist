from flask import Flask
from api import api_bp
from views import views_bp
from db import init_db, init_app as init_db_app

def create_app():
    app = Flask(__name__)
    app.config['DATABASE'] = 'tasklist.db'
    
    # Initialize database utilities
    init_db_app(app)
    
    # Register the API blueprint
    app.register_blueprint(api_bp)
    app.register_blueprint(views_bp)
    
    # Initialize database from schema.sql
    with app.app_context():
        init_db()  # This will use your schema.sql file
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)