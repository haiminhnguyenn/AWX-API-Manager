from flask import Blueprint

bp = Blueprint('v2', __name__)

from app.blueprints.api.v2 import routes