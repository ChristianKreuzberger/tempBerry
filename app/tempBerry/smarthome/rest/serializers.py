from rest_framework import serializers

from tempBerry.smarthome.models import Room


class RoomSerializer(serializers.ModelSerializer):
    """
    Serializer for rooms
    """
    class Meta:
        model = Room
        fields = ('id', 'name', 'comment', 'created_at', 'public',
                  'has_temperature', 'has_humidity', 'has_air_pressure')
        read_only_fields = ('created_at', )
