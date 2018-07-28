from os import path

class Config(object):
    pass

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+path.join(path.pardir, 'database.db')
    SQLALCHEMY_ECHO = True