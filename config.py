import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = True
    MONGO_DB_NAME = 'crypto_app_database'
    MONGO_DB_COLLECTION_NAME = 'phone_gcmid_col'
    MONGO_DB_IP = 'localhost'
    MONGO_DB_PORT = 27017
    DB_EXAMPLE_VALUES = [('123121','Registrationid1'),('1231212','Registrationidtwo')]
    GOOGLE_API="AIzaSyC8aJTsVngyjgiH9t_tjyGMzQZ3TLG5awY"
    DRY_RUN_API=False

    @staticmethod
    def init_app(app):
        pass

class TestingConfig(Config):
    TESTING = True
    MONGO_DB_NAME = 'crypto_app_test_database'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    DRY_RUN_API=True
    @classmethod
    def init_app(cls,app):
        print("Using TestingConfig")


class DevelopmentConfig(Config):
    DEBUG = True
    @classmethod
    def init_app(cls, app):
        import logging
        from logging import StreamHandler
        stream_handler = StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        stream_handler.setFormatter(formatter)
        app.logger.addHandler(stream_handler)
        app.logger.debug("Using DevelopmentConfig")



class HerokuConfig(Config):
    SSL_DISABLE =False
    DEBUG = False
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)
        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)    
        app.logger.addHandler(file_handler)
        app.logger.warning("Using HerokuConfig")



config = {
    'development': DevelopmentConfig,
    'heroku': HerokuConfig,
    'testing':TestingConfig,
    'default': DevelopmentConfig
}
