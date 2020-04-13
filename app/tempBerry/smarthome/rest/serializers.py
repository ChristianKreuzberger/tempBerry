from rest_framework import serializers

from tempBerry.smarthome.models import Room, SmartHome, Sensor, AbstractDataEntry


class SensorSerializer(serializers.ModelSerializer):
    """
    Serializer for Sensors
    """
    class Meta:
        model = Sensor
        fields = (
            'id', 'name', 'created_at', 'last_updated_at', 'comment', 'public', 'type'
        )


class GenericDataSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    source = serializers.CharField()
    created_at = serializers.DateTimeField()


class RoomSerializer(serializers.ModelSerializer):
    """
    Serializer for rooms
    """
    sensors = SensorSerializer(many=True)

    live_data = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ('id', 'name', 'comment', 'created_at', 'public', 'sensors', 'live_data',
                  'has_temperature', 'has_humidity', 'has_air_pressure')
        read_only_fields = ('created_at', )

    def get_live_data(self, obj):
        if not hasattr(obj, 'live_data'):
            return None

        data = []

        from tempBerry.temperatures.models import TemperatureDataEntry
        from tempBerry.binarySensor.models import BinarySensorData

        from tempBerry.temperatures.rest.serializers import TemperatureDataEntrySerializer
        from tempBerry.binarySensor.rest.serializers import BinarySensorDataSerializer

        # Convert into objects "live"
        for instance in obj.live_data:
            if isinstance(instance, TemperatureDataEntry):
                data.append(TemperatureDataEntrySerializer(instance).data)
            elif isinstance(instance, BinarySensorData):
                data.append(BinarySensorDataSerializer(instance).data)
            else:
                data.append(GenericDataSerializer(instance).data)

        return data


class MinimalisticSmartHomeSerializer(serializers.Serializer):
    """
    Minimalistic Serializer for SmartHome
    """
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
