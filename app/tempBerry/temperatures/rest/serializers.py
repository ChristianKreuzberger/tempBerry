from django.db.models import Avg
from django.utils import timezone

from rest_framework import serializers

from tempBerry.smarthome.models import Room
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
        read_only_fields = ('created_at', 'sensor_id', 'real_sensor', 'room')


class RoomLiveDataSerializer(serializers.ModelSerializer):
    """
    Serializer for rooms
    """

    live_data = TemperatureDataEntrySerializer(many=False)

    average_last_hour = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ('id', 'name', 'comment', 'created_at', 'public', 'live_data',
                  'has_temperature', 'has_humidity', 'has_air_pressure', 'average_last_hour')
        read_only_fields = ('created_at', 'live_data')

    def get_average_last_hour(self, object):

        aggregates = object.temperaturedataentry_set.order_by('-created_at').filter(
            created_at__gte=timezone.now() - timezone.timedelta(hours=1)
        ).aggregate(
            temperature=Avg('temperature'),
            humidity=Avg('humidity'),
            air_pressure=Avg('air_pressure')
        )

        return aggregates