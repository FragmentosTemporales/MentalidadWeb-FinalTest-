import os
from datetime import timedelta


basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    """ Base configuration application class """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "123456")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES_HOURS", 12))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES_DAYS", 6))
    )
    RECORDS_PER_PAGE = int(os.environ.get("RECORDS_PER_PAGE", 15))
    SECRET_KEY = os.environ.get("SECRET_KEY", "123456")


class ProductionConfig(BaseConfig):
    """ Production configuration class """
    pass


class DevConfig(BaseConfig):
    """ Development configuration class """
    db_user = os.environ.get("POSTGRES_USER", "admin")
    db_pass = os.environ.get("POSTGRES_PASSWORD", "pw")
    db_name = os.environ.get("POSTGRES_DB", "postgres")
    db_host = os.environ.get("POSTGRES_HOST", "postgres")
    db_port = os.environ.get("POSTGRES_PORT", "5432")
    SQLALCHEMY_DATABASE_URI = ("postgresql://{}:{}@{}:{}/{}".format(
        db_user, db_pass, db_host, db_port, db_name
    ))


class TestConfig(BaseConfig):
    """ Testing configuration class """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        basedir, "..", 'test.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    "dev": DevConfig,
    "prod": ProductionConfig,
    "test": TestConfig
}
