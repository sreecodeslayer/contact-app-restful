from .paginator import paginate
from ..config import configuration
import os


def loadconf():
    '''
    Load the server configuration
    '''
    env = os.getenv('CONTACTS_ENV', 'dev').lower()
    config = configuration[env]
    return config
