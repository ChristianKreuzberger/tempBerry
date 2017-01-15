#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WSGI config for tempBerry project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ['LANG']='en_US.UTF-8'
os.environ['LC_ALL']='en_US.UTF-8'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tempBerry.settings")

application = get_wsgi_application()
