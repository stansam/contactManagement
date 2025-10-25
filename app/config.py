import os 

class Config:
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    SQLALCHEMY_DATABASE_URI = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@cluster0.331zabm.mongodb.net/?appName=Cluster0"