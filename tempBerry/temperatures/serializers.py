from temperatures.models import TemperatureDataEntry, UnknownDataEntry, Room
from rest_framework import serializers


class TemperatureDataEntrySerializer(serializers.ModelSerializer):
    """
    Serializers for temperature data entries
    """
    class Meta:
        model = TemperatureDataEntry
        fields = ('id', 'sensor_id', 'temperature', 'humidity', 'created_at', 'source', 'battery')
        read_only_fields = ('created_at', )


class RoomSerializer(serializers.ModelSerializer):
    """
    Serializer for rooms
    """
    class Meta:
        model = Room
        fields = ('id', 'sensor_id', 'name', 'comment', 'created_at')
        read_only_fields = ('created_at', )
