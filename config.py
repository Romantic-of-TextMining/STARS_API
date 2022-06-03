import os

API_HOST_DEFAULT = "127.0.0.1"

def get_postgres_uri():
    host = os.environ.get("DB_HOST", "localhost")
    port = 5432 if host == "localhost" else 5432
    password = os.environ.get("DB_PASSWORD", "")
    user, db_name = "allocation", "allocation"
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_api_url():
    host = os.environ.get("API_HOST", API_HOST_DEFAULT)
    port = 5000 if host == API_HOST_DEFAULT else 80
    return f"http://{host}:{port}"

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    #SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    #MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    #MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    #MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
    #    ['true', 'on', '1']
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    #MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    #FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    #FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    #FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    #SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    #    'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    #SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
    #    'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
       'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
