from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushServerError,
)
import requests
from requests.exceptions import ConnectionError, HTTPError
from userauth.models import PushToken
from microservices.rollbar_integration import *


# Optionally providing an access token within a session if you have enabled push security
session = requests.Session()
session.headers.update(
    {
        "Authorization": f"Bearer TVqs827jyS5cZ1tvqgpds64LrMDBZXyOhEFPPlRJ",
        "accept": "application/json",
        "accept-encoding": "gzip, deflate",
        "content-type": "application/json",
    }
)


def send_push_message(token, title, message, extra=None):
    try:
        response = PushClient(session=session).publish(
            PushMessage(to=token, title=title, body=message,
                        data=extra, priority='high', sound='default')
        )
        handle_push_response(response)
    except PushServerError as exc:
        handle_push_server_error(token, message, extra, exc)
        raise
    except DeviceNotRegisteredError:
        handle_device_not_registered(token, message, extra)
    except (ConnectionError, HTTPError) as exc:
        handle_connection_error(token, message, extra)
        raise


def handle_push_response(response):
    # Handle the push response as needed
    if response.status == "ok":
        print("Push notification sent successfully.")
    else:
        print(
            f"Failed to send push notification. Response: {response.__dict__}")


def handle_push_server_error(token, message, extra, exc):
    # Handle push server error as needed
    rollbar.report_exc_info(
        extra_data={
            "token": token,
            "message": message,
            "extra": extra,
            "errors": exc.errors,
            "response_data": exc.response_data,
        }
    )
    raise


def handle_device_not_registered(token, message, extra):
    # Mark the push token as inactive or handle accordingly
    PushToken.objects.filter(token=token).update(active=False)


def handle_connection_error(token, message, extra):
    # Handle connection error or HTTP error
    rollbar.report_exc_info(
        extra_data={"token": token, "message": message, "extra": extra}
    )
    raise
