from rest_framework import status
from rest_framework.response import Response


def create_success_response(data=None, message=None, status_code=None):
    response = {
        'success': True,
        'message': message,
        'data': data or []
    }
    return Response(response, status=status_code)


def create_error_response(message=None, data=None, status_code=None):
    response = {
        'success': False,
        'message': message,
        'data': data or []
    }
    return Response(response, status=status_code)
