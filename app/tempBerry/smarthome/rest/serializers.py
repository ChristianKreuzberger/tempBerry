from rest_framework import serializers

from tempBerry.smarthome.models import Room, SmartHome, Sensor, AbstractDataEntry

class AbstractDataEntrySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    source = serializers.CharField()
    created_at = serializers.DateTimeField()


class SensorSerializer(serializers.ModelSerializer):
    """
    Serializer for Sensors
    """
    live_data = serializers.SerializerMethodField()

    class Meta:
        model = Sensor
        fields = (
            'id', 'name', 'created_at', 'last_updated_at', 'comment', 'public', 'type', 'live_data',
        )

    def get_live_data(self, obj):
        if not hasattr(obj, 'live_data') or not obj.live_data:
            return None

        from tempBerry.temperatures.models import TemperatureDataEntry
        from tempBerry.binarySensor.models import BinarySensorData

        from tempBerry.temperatures.rest.serializers import TemperatureDataEntrySerializer
        from tempBerry.binarySensor.rest.serializers import BinarySensorDataSerializer

        # Convert into appropriate format
        if isinstance(obj.live_data, TemperatureDataEntry):
            return TemperatureDataEntrySerializer(obj.live_data).data
        elif isinstance(obj.live_data, BinarySensorData):
            return BinarySensorDataSerializer(obj.live_data).data
        else:
            return AbstractDataEntrySerializer(obj.live_data).data


class RoomSerializer(serializers.ModelSerializer):
    """
    Serializer for rooms
    """
    sensors = SensorSerializer(many=True)

    class Meta:
        model = Room
        fields = ('id', 'name', 'comment', 'created_at', 'public', 'sensors',
                  'has_temperature', 'has_humidity', 'has_air_pressure')
        read_only_fields = ('created_at', )


class MinimalisticSmartHomeSerializer(serializers.Serializer):
    """
    Minimalistic Serializer for SmartHome
    """
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
