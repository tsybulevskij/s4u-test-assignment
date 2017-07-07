from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    if response is not None:
        response.data = {
            'error': True,
            'code': response.status_code,
            'message': exc.detail
        }

    return response
