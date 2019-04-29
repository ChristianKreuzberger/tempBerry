from rest_framework import serializers

from tempBerry.binarySensor.models import BinarySensorData


class BinarySensorDataSerializer(serializers.ModelSerializer):
    """
    Serializers for binary data
    """
    class Meta:
        model = BinarySensorData
        fields = ('id', 'sensor_id', 'binary_state', 'created_at', 'room', 'source',)
        read_only_fields = ('created_at', )
