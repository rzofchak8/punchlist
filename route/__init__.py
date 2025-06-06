from flask import Blueprint
from db import get_db  # Import shared get_db function

views_bp = Blueprint("views", __name__)

# from . import users, tasks
