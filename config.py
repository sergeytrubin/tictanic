import os


class BaseConfig(object):
    """Standard configuration options"""
    DEBUG = True
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    db_uri = 'postgresql://tictanic:devpassword@postgres:5432/tictanic'
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')
    WTF_CSRF_ENABLED = False
    DATABASE_CONNECT_OPTIONS = {}
    THREADS_PER_PAGE = 2
    # SERVER_NAME = 'localhost:8000'
    SECRET_KEY = 'insecurekeyfordev'
    BCRYPT_LOG_ROUNDS = 12


class TestConfig(BaseConfig):
    """Configuration for general testing"""
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    WTF_CSRF_ENABLED = False
    LOGIN_DISABLED = True
    BCRYPT_LOG_ROUNDS = 4


class AuthTestConfig(TestConfig):
    """For testing authentication we want to require login to check validation works"""
    LOGIN_DISABLED = True
