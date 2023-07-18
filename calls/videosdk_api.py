import jwt
import datetime
import requests

VIDEOSDK_API_KEY = "YOUR_API_KEY"
VIDEOSDK_SECRET_KEY = "YOUR_SECRET_KEY"
TOKEN_EXPIRATION_SECONDS = 7200


def generate_videosdk_token():
    expiration = datetime.datetime.now(
    ) + datetime.timedelta(seconds=TOKEN_EXPIRATION_SECONDS)
    payload = {
        'exp': expiration,
        'apikey': VIDEOSDK_API_KEY,
        'permissions': ['allow_join', 'allow_mod'],
    }
    token = jwt.encode(
        payload=payload, key=VIDEOSDK_SECRET_KEY, algorithm='HS256')
    return token.decode('UTF-8')


def create_videosdk_room(custom_room_id):
    token = generate_videosdk_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    url = "https://api.videosdk.live/v2/rooms"
    data = {
        "region": "sg001",
        "customRoomId": custom_room_id,
        "webhook": "see example",
        "autoCloseConfig": "see example"
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()


def end_videosdk_room(room_id):
    token = generate_videosdk_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    url = "https://api.videosdk.live/v2/rooms/deactivate"
    data = {
        "roomId": room_id
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()
