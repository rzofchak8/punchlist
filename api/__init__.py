from flask import Blueprint
# from db import get_db  # Import shared get_db function

api_bp = Blueprint("api", __name__, url_prefix="/api")
from . import categories, houses, photos, rooms, tasks, users

# Make get_db available to all API modules
# __all__ = ['api_bp', 'get_db']