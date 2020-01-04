from rest_framework import serializers

from tempBerry.smarthome.models import Room, SmartHome


class RoomSerializer(serializers.ModelSerializer):
    """
    Serializer for rooms
    """
    class Meta:
        model = Room
        fields = ('id', 'name', 'comment', 'created_at', 'public',
                  'has_temperature', 'has_humidity', 'has_air_pressure')
        read_only_fields = ('created_at', )


class MinimalisticSmartHomeSerializer(serializers.Serializer):
    """
    Minimalistic Serializer for SmartHome
    """
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
