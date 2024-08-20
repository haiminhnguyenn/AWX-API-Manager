from flask import Flask
from config import Config
from app.extensions import db, jwt

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    
    from app.blueprints.api.kong_gateways import bp as kong_gateways_bp
    app.register_blueprint(kong_gateways_bp, url_prefix="/api/kong_gateways")
    
    from app.blueprints.api.v1 import bp as v1_bp
    app.register_blueprint(v1_bp, url_prefix="/api/v1")

    return app