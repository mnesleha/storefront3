import os
import dj_database_url
from .common import *

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['moshbuy-marek-prod-d64e612dbf44.herokuapp.com']

DATABASES = {
    'default': dj_database_url.config()
}
