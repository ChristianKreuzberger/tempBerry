from tempBerry.settings.base import *

# ensure that debug is false
DEBUG = False

# ensure whitenoise static file storage is used
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
