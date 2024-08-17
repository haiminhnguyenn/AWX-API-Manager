from flask import Flask
from config import Config
from app.extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    
    # Register blueprints here
    from app.blueprints.api.kong_gateways import bp as kong_gateways_bp
    app.register_blueprint(kong_gateways_bp, url_prefix="/api/kong_gateways")
    
    from app.blueprints.api.v2 import bp as v2_bp
    app.register_blueprint(v2_bp, url_prefix="/api/v2")

    return app


app = create_app()