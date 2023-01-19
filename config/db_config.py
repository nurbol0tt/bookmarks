"""Flask config class."""
from .base_config import BaseConfig


class DatabaseConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///project.db'
