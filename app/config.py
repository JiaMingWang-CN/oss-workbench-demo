import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:
    SECRET_KEY = "dev-secret-123"
    DATABASE = os.path.join(BASE_DIR, "instance", "notes.sqlite")
    EXPORT_DIR = os.path.join(BASE_DIR, "instance", "exports")
    TESTING = False
