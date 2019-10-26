from tempBerry.settings.base import *

# debugging is enabled for the dev version :)
DEBUG = True

# automatically enable certain hosts
CORS_ORIGIN_REGEX_WHITELIST = (
    '^(http?://)?localhost$',  # localhost
    '^(http?://)?127\.0\.0\.1$',  # 127.0.0.1
    '^(http?://)?0\.0\.0\.0$',  # 0.0.0.0
    '^(http?://)?tempberry.local:(\d+)$',  # tempberry.local:any port
    '^(http?://)?localhost:(\d+)$',  # localhost:any port
    '^(http?://)?127\.0\.0\.1:(\d+)$',  # 127.0.0.1:any port
    '^(http?://)?0\.0\.0\.0:(\d+)$',  # 0.0.0.0:any port
)

# allow all hosts for dev setup
ALLOWED_HOSTS = [
    "*"
]
