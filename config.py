import os


class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = '618ca39a0f42eac1c87cd91a842105dc0b08c634e4d98f4f96ce1e3fc6dcbd53'


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    DEBUG = False


DATABASE_SETTINGS = {
    'host': '127.0.0.1',
    'user': 'parsdata',
    'password': 'it.r4min.r4min',
    'database': 'parsdata',
}