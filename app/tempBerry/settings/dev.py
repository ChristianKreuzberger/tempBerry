from tempBerry.settings.base import *

DEBUG = True

SECRET_KEY = os.getenv('SECRET_KEY', default="some_random_secret_key")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tempberry',
        'USER': 'tempberry',
        'PASSWORD': 'tempberry',
        'HOST': '127.0.10.1',
        'PORT': '3306'
    }
}

# allow all hosts for now
ALLOWED_HOSTS = [
    "*"
]
