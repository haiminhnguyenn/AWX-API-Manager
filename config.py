class Config:
    SECRET_KEY = "secret"
    JWT_SECRET_KEY = "jwt"
    SQLALCHEMY_DATABASE_URI = "postgresql://kongservice_dev:kongservice_dev@localhost:5432/kongservice_dev" 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = "amqp://localhost"      #amqp://guest:guest@localhost:5672//