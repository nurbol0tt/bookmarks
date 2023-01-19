"""Flask config class."""
import os
from .db_config import BaseConfig


class MailConfig(BaseConfig):
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587  # 465
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
