import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY='9OLWxND4o83j4K4iuopO'
    SQLALCHEMY_DATABASE_URI='sqlite:///db.sqlite'

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    				


class TestingConfig(Config):
    TESTING = True
    DEBUG=True		
