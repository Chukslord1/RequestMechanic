from rest_framework import serializers
from .models import Call, Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class CallSerializer(serializers.ModelSerializer):
    room = RoomSerializer()

    class Meta:
        model = Call
        fields = '__all__'
