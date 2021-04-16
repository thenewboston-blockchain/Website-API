import logging

from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data['status_code'] = response.status_code
        # logs detail data from the exception being handled
        logging.error(f'Original error detail and callstack: {exc}')
        response.data['status_code'] = response.status_code
    return response
