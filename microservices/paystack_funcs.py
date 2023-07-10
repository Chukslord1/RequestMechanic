import requests
from django.conf import settings
from rest_framework import status
from .response import create_error_response


# def charge_authorization(authorization_code, email, amount):
#     url = 'https://api.paystack.co/transaction/charge_authorization'
#     headers = {
#         'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
#         'Content-Type': 'application/json'
#     }
#     data = {
#         'authorization_code': authorization_code,
#         'email': email,
#         'amount': amount,
#     }

#     response = requests.post(url, headers=headers, json=data)
#     return response.json()
def charge_authorization(authorization_code, email, amount):
    url = 'https://api.paystack.co/transaction/charge_authorization'
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'authorization_code': authorization_code,
        'email': email,
        'amount': amount,
    }

    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
    print(response_data)

    if response.status_code == 200:
        return response_data
    else:
        error_message = response_data.get(
            'message', 'Error processing payment')
        return create_error_response(error_message, response_data, status_code=response.status_code)


def initialize_transaction(email, amount):
    url = 'https://api.paystack.co/transaction/initialize'
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'email': email,
        'amount': amount,
    }

    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()

    if response_data.get('status'):
        return response_data
    else:
        error_message = response_data.get(
            'message', 'Failed to create authorization URL')
        return create_error_response(error_message, response_data, status_code=response.status_code)


# Add other functions related to Paystack here
