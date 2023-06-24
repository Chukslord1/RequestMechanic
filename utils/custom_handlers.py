from django.http import JsonResponse
from rest_framework import status


def handler404(request, exception):
    response_data = {
        'error': 'Not found',
        'message': 'The requested resource could not be found.',
        'code':'404'
    }
    return JsonResponse(response_data, sstatus=status.HTTP_404_NOT_FOUND)
