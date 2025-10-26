import os 

class Config:
    DEBUG = True
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    DB_USER = os.environ.get("DB_USER") or "cynthiacheptoo26_db_user"
    DB_PASSWORD = os.environ.get("DB_PASSWORD") or "tynee123"
    DB_NAME = os.environ.get("DB_NAME") or "flask_mongodb_assignment"
    MONGO_URI = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@cluster0.331zabm.mongodb.net/?appName=Cluster0&authSource=admin"
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_RECORD_QUERIES = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')