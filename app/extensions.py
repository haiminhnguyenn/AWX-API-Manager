from flask_sqlalchemy import SQLAlchemy
from app.models.base import Base
from flask_jwt_extended import JWTManager

db = SQLAlchemy(model_class=Base)

jwt = JWTManager()