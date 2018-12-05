import os


class Development:
    DEBUG = True
    SECRET_KEY = "changeme"

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/contacts'

    # Suppress SQLALCHEMY_TRACK_MODIFICATIONS overhead warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Production(Development):
    DEBUG = False
    SECRET_KEY = "sup3rs3cr3tk3yf0rPr0duct10N"
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'SQLALCHEMY_DATABASE_URI',
        'postgresql://localhost/contacts'
    )


configuration = {
    'dev': Development,
    'production': Production
}
