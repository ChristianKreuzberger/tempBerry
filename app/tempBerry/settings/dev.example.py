from tempBerry.settings.base import *

DEBUG = True

# PLEASE ENTER A SECRET KEY HERE
SECRET_KEY = ""

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

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis.tempberry.local:6379/",
    }
}