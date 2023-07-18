from rest_framework import serializers
from userauth.models import User
from .models import Mechanic, Request


class MechanicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'car_brand',
                  'car_model', 'completed_registration', 'is_available',
                  'rating', 'rate']


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id', 'user', 'car_brand', 'description', 'created_at']


class MatchMechanicSerializer(serializers.ModelSerializer):
    user = MechanicSerializer()

    class Meta:
        model = Mechanic
        fields = ['user']
