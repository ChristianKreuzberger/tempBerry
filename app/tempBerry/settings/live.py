import os
from tempBerry.settings.base import *


DEBUG = False
SECRET_KEY = os.getenv('SECRET_KEY')
