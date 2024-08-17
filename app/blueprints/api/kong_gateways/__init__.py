from flask import Blueprint

bp = Blueprint('kong_gateways', __name__)

from app.blueprints.api.kong_gateways import routes