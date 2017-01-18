from temperatures.models import TemperatureDataEntry, UnknownDataEntry
from rest_framework import serializers


class TemperatureDataEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperatureDataEntry
        fields = ('id', 'sensor_id', 'temperature', 'humidity', 'created_at', 'source', 'battery')
        readonly_fields = ('created_at', )
