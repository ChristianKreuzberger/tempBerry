from tempBerry.settings.base import *

import pymysql

pymysql.install_as_MySQLdb()

DEBUG = True

SECRET_KEY = os.getenv('SECRET_KEY', default="some_random_secret_key")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tempberry',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}

# allow all hosts for now
ALLOWED_HOSTS = [
    "*"
]
