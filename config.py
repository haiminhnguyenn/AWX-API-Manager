import os

class Config:
    # SECRET_KEY = os.environ.get("SECRET_KEY")
    # JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    SECRET_KEY = "secretkey"
    JWT_SECRET_KEY = "jwt"
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:26032003@localhost:5432/awx_api_manager_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # CELERY_BROKER_URL = "pyamqp://guest@localhost//"
    # CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
    # AWX_HOST = os.getenv("AWX_HOST")
    # AWX_PORT = os.getenv("AWX_PORT")
    # AWX_TEMPLATE_ID = os.getenv("AWX_TEMPLATE_ID")
    # AWX_USERNAME = os.getenv("AWX_USERNAME")
    # AWX_PASSWORD = os.getenv("AWX_PASSWORD")