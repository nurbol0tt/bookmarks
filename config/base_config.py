"""Flask config class."""
import os


class BaseConfig:
    """Base config vars."""
    SECRET_KEY = '80913d1e52beed14ccdadad1502577d1'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///project.db'
