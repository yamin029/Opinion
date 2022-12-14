from base.models import Room
from django.rest_framework import ModelSerializers

class RoomSerializers():
    class Meta:
        model: Room
        fields : "__all__"