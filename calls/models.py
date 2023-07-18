from django.db import models
from userauth.models import User


class Call(models.Model):
    caller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='outgoing_calls')
    participant = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='incoming_calls')
    room = models.OneToOneField('Room', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Room(models.Model):
    room_id = models.CharField(max_length=255)
    custom_room_id = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(User)
