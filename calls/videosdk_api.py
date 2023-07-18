import jwt
import datetime
import requests

VIDEOSDK_API_KEY = "91f5193d-a884-43ac-aaf5-be36b1f6a65b"
VIDEOSDK_SECRET_KEY = "701a6f63f22e42ecfffc3a40ed9bc01c0f08b240106f444fc084c8cddea6d9fb"
TOKEN_EXPIRATION_SECONDS = 7200


def generate_videosdk_token():

    expiration_in_seconds = TOKEN_EXPIRATION_SECONDS
    expiration = datetime.datetime.now() + datetime.timedelta(seconds=expiration_in_seconds)

    # token = jwt.encode(payload={
    #     'exp': expiration,
    #     'apikey': VIDEOSDK_API_KEY,
    #     'permissions': ['allow_join', 'allow_mod'],
    # }, key=VIDEOSDK_SECRET_KEY, algorithm='HS256')
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGlrZXkiOiI2OWU3ZTgzYS1iYmUyLTQ5YmUtODI4Mi05ZTQ1ODExZDUyNTIiLCJwZXJtaXNzaW9ucyI6WyJhbGxvd19qb2luIl0sImlhdCI6MTY4OTY4Mzg3NSwiZXhwIjoxNjkwMjg4Njc1fQ.HIIUY-NR7K9st845E7WKxuz5NhoaPqEvBDJBs-Ud2Qs'
    return token


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
    print(response.json())


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
