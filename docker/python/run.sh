#!/bin/bash

gunicorn tempBerry.wsgi --access-logfile - --error-logfile - -b 0.0.0.0:8000
