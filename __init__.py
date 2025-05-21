from flask import Flask
from .house import house_bp
from .room import room_bp
from .photo import photo_bp
from .user import user_bp
from .task import task_bp
from .tasklist import tasklist_bp
from .tasktype import tasktype_bp

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(house_bp)
    app.register_blueprint(room_bp)
    app.register_blueprint(photo_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(tasklist_bp)
    app.register_blueprint(tasktype_bp)

    return app
