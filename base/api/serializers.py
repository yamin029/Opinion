from base.models import Room
from rest_framework import serializers

class RoomSerializers(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'