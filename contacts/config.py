import os
from datetime import timedelta


class Development:
    DEBUG = True
    SECRET_KEY = "changeme"
    JWT_ACCESS_TOKEN_EXPIRES = False

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres'\
        '@localhost/contacts'

    # Suppress SQLALCHEMY_TRACK_MODIFICATIONS overhead warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Production(Development):
    DEBUG = False
    SECRET_KEY = "sup3rs3cr3tk3yf0rPr0duct10N"
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'SQLALCHEMY_DATABASE_URI',
        'postgresql://localhost/contacts'
    )
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(7)


configuration = {
    'dev': Development,
    'production': Production
}
