from rest_framework.views import exception_handler as drf_handler


def exception_handler(exc, context):
    response = drf_handler(exc, context)
    if response is not None:
        response.data = {'error': {'code': {400: 'invalid', 401: 'unauthenticated', 403: 'forbidden', 404: 'not_found', 409: 'conflict'}.get(response.status_code, 'error'), 'details': response.data}}
    return response
