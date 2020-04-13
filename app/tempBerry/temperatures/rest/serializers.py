from rest_framework import serializers

from tempBerry.temperatures.models import TemperatureDataEntry


class TemperatureDataEntrySerializer(serializers.ModelSerializer):
    """
    Serializers for temperature data entries
    """
    class Meta:
        model = TemperatureDataEntry
        fields = (
            'id',
            'sensor_id',
            'temperature',
            'humidity',
            'air_pressure',
            'created_at',
            'room',
            'real_sensor',
            'source',
            'battery'
        )
        read_only_fields = ('created_at', 'real_sensor', 'room')
