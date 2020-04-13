from datetime import timedelta

from django.core.cache import cache
from django.db.models import Avg, Max, Min, Count
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from tempBerry.smarthome.models import Room
from tempBerry.smarthome.rest.serializers import RoomSerializer
from tempBerry.temperatures.models import TemperatureDataEntry
from tempBerry.temperatures.rest.serializers import TemperatureDataEntrySerializer


class TemperatureDataEntryViewSet(viewsets.ModelViewSet):
    """
    Viewset for temperature data
    """
    serializer_class = TemperatureDataEntrySerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('room_id', 'sensor_id', )

    def get_queryset(self):
        end_date = timezone.now()
        start_date = end_date - timedelta(hours=96)
        return TemperatureDataEntry.objects.filter(
            created_at__range=(start_date, end_date)
        ).order_by('created_at')


class RoomDataViewSet(viewsets.ModelViewSet):
    """
    Viewset for room
    """
    serializer_class = RoomSerializer
    filter_backends = (DjangoFilterBackend,)
    queryset = Room.objects.all()

    @action(detail=True, methods=['GET'])
    def stats(self, request, pk):
        """ return some stats of this room """
        # find the first and last entry of this room
        room = Room.objects.get(pk=pk)

        latest_entry = room.temperaturedataentry_set.all().latest("created_at")

        cnt = room.temperaturedataentry_set.count()

        avg = room.temperaturedataentry_set.all().aggregate(
            Avg('temperature'),
            Avg('humidity')
        )

        data = {
            'latest': TemperatureDataEntrySerializer(latest_entry).data,
            'avg_temperature': avg['temperature__avg'],
            'avg_humidity': avg['humidity__avg'],
            'cnt': cnt
        }

        return Response(data)

    @action(detail=True, methods=['GET'])
    def aggregates_24h(self, request, pk):
        end_date = timezone.now()
        start_date = end_date - timedelta(hours=24)

        room = Room.objects.get(pk=pk)

        qs = room.temperaturedataentry_set.filter(
            created_at__range=(start_date, end_date)
        ).aggregate(
            max_temperature=Max('temperature'),
            min_temperature=Min('temperature'),
            avg_temperature=Avg('temperature'),
            max_humidity=Max('humidity'),
            min_humidity=Min('humidity'),
            avg_humidity=Avg('humidity'),
            max_air_pressure=Max('air_pressure'),
            min_air_pressure=Min('air_pressure'),
            avg_air_pressure=Avg('air_pressure'),
        )

        return Response(qs)

    @action(detail=True, methods=['GET'])
    def aggregates_1month(self, request, pk):
        end_date = timezone.now()
        start_date = end_date - timedelta(weeks=4)

        room = Room.objects.get(pk=pk)

        qs = room.temperaturedataentry_set.filter(
            created_at__range=(start_date, end_date)
        ).aggregate(
            max_temperature=Max('temperature'),
            min_temperature=Min('temperature'),
            avg_temperature=Avg('temperature'),
            max_humidity=Max('humidity'),
            min_humidity=Min('humidity'),
            avg_humidity=Avg('humidity'),
            max_air_pressure=Max('air_pressure'),
            min_air_pressure=Min('air_pressure'),
            avg_air_pressure=Avg('air_pressure'),
        )

        return Response(qs)
