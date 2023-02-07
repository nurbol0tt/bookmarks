"""Flask config class."""
import os
from .db_config import BaseConfig


class MailConfig(BaseConfig):
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587  # 465
    MAIL_USERNAME = 'nurbolot664@gmail.com'
    MAIL_PASSWORD = 'racbswrtlyhipiol'
    MAIL_USE_TLS = True
