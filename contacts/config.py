import os
from datetime import timedelta


class Development:
    DEBUG = True
    SECRET_KEY = "changeme"

    # Skipping the below configuration would trigger a 500
    # on bad api request with no auth headers case
    # Read more at flask jwt extended issue 86
    # https://github.com/vimalloc/flask-jwt-extended/issues/86
    PROPAGATE_EXCEPTIONS = True

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


class Testing(Development):
    DEBUG = True
    TESTING = True
    SECRET_KEY = "testsecret"
    JWT_ACCESS_TOKEN_EXPIRES = False

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres'\
        '@localhost/contacts_test'

    # Suppress SQLALCHEMY_TRACK_MODIFICATIONS overhead warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False


configuration = {
    'dev': Development,
    'production': Production,
    'test': Testing
}
