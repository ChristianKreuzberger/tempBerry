from rest_framework import serializers
from tempBerry.temperatures.models import TemperatureDataEntry, Room


class TemperatureDataEntrySerializer(serializers.ModelSerializer):
    """
    Serializers for temperature data entries
    """
    class Meta:
        model = TemperatureDataEntry
        fields = ('id', 'sensor_id', 'temperature', 'humidity', 'air_pressure', 'created_at', 'room', 'source', 'battery')
        read_only_fields = ('created_at', )


class RoomSerializer(serializers.ModelSerializer):
    """
    Serializer for rooms
    """
    class Meta:
        model = Room
        fields = ('id', 'name', 'comment', 'created_at', 'public',
                  'has_temperature', 'has_humidity', 'has_air_pressure')
        read_only_fields = ('created_at', )


class RoomLiveDataSerializer(serializers.ModelSerializer):
    """
    Serializer for rooms
    """

    live_data = TemperatureDataEntrySerializer(many=False)

    class Meta:
        model = Room
        fields = ('id', 'name', 'comment', 'created_at', 'public', 'live_data')
        read_only_fields = ('created_at', 'live_data')
