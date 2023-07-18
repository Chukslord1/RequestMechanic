from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Call, Room
from .serializers import CallSerializer
from .videosdk_api import generate_videosdk_token, create_videosdk_room, end_videosdk_room
    

VIDEOSDK_API_KEY = "YOUR_API_KEY"
VIDEOSDK_SECRET_KEY = "YOUR_SECRET_KEY"
TOKEN_EXPIRATION_SECONDS = 7200


class InitiateCallView(APIView):
    def post(self, request):
        caller_id = request.data.get('caller_id')
        participant_id = request.data.get('participant_id')

        try:
            caller = User.objects.get(id=caller_id)
            participant = User.objects.get(id=participant_id)
        except User.DoesNotExist:
            return Response({'error': 'Invalid caller or participant ID'}, status=status.HTTP_404_NOT_FOUND)

        # Replace with your custom room ID logic
        room_data = create_videosdk_room(custom_room_id="your_custom_room_id")

        room_id = room_data.get('roomId')
        custom_room_id = room_data.get('customRoomId')

        room = Room.objects.create(
            room_id=room_id, custom_room_id=custom_room_id)
        room.participants.add(caller, participant)

        call = Call.objects.create(
            caller=caller, participant=participant, room=room)

        serializer = CallSerializer(call)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EndCallView(APIView):
    def post(self, request):
        room_id = request.data.get('room_id')

        try:
            room = Room.objects.get(room_id=room_id)
        except Room.DoesNotExist:
            return Response({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)

        end_videosdk_room(room_id)  # End the Videosdk room

        room.is_active = False
        room.save()

        return Response({'message': 'Call ended successfully'}, status=status.HTTP_200_OK)
