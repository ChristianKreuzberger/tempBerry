from tempBerry.settings.base import *

DEBUG = True

SECRET_KEY = os.getenv('SECRET_KEY', default="some_random_secret_key")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tempberry',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}

# allow all hosts for now
ALLOWED_HOSTS = [
    "*"
]
