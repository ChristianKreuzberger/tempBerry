from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError, PermissionDenied
import django.core.exceptions

import logging


def custom_exception_handler(exc, context):
    # Handle Django Validation Errors (convert them into Django REST Validation Errors)
    if type(exc) is django.core.exceptions.ValidationError:
        if hasattr(exc, "message_dict"):
            exc = ValidationError(exc.message_dict)
        elif hasattr(exc, "messages"):
            exc = ValidationError(exc.messages)
        else:
            exc = ValidationError(exc)
    # Handle Django Permission Errors (convert t hem into Django REST Permission Errors)
    elif type(exc) is django.core.exceptions.PermissionDenied:
        if len(exc.args) >= 1:
            exc = PermissionDenied(exc)
        else:
            exc = PermissionDenied()

    # Call REST framework's default exception handler to get the standard error response
    response = exception_handler(exc, context)

    return response
