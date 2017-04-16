from datetime import datetime, timedelta
from django.db.models import Avg, Max, Min
from django.utils import timezone
from django.core.cache import cache

from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from temperatures.models import TemperatureDataEntry, UnknownDataEntry
from temperatures.serializers import TemperatureDataEntrySerializer


class TemperatureDataEntryViewSet(viewsets.ModelViewSet):
    """
    Viewset for temperature data
    """
    serializer_class = TemperatureDataEntrySerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('sensor_id', )

    def get_queryset(self):
        end_date = timezone.now()
        start_date = end_date - timedelta(hours=96)
        return TemperatureDataEntry.objects.filter(
            created_at__range=(start_date, end_date)
        )

    def get_aggregates_24h(self, sensor_id):
        end_date = timezone.now()
        start_date = end_date - timedelta(hours=24)
        qs = TemperatureDataEntry.objects.filter(
            sensor_id=sensor_id,
            created_at__range=(start_date, end_date)
        ).aggregate(
            max_temperature=Max('temperature'),
            min_temperature=Min('temperature'),
            avg_temperature=Avg('temperature'),
            max_humidty=Max('humidity'),
            min_humidty=Min('humidity'),
            avg_humidty=Avg('humidity'),
        )

    @list_route(methods=['GET'])
    def latest_old(self, request):
        # get all sensor ids
        list = TemperatureDataEntry.objects.order_by('-created_at', 'sensor_id').values('created_at', 'sensor_id')[:20]

        qs = TemperatureDataEntry.objects.none()

        sensor_ids = []

        for entry in list:
            if entry['sensor_id'] in sensor_ids or entry['sensor_id'] == '0' or entry['sensor_id'] == 0:
                continue
            sensor_ids.append(entry['sensor_id'])
            qs = qs | TemperatureDataEntry.objects.filter(created_at=entry['created_at'], sensor_id=entry['sensor_id'])

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


    @list_route(methods=['GET'])
    def latest(self, request):
        """
        Display latest data by reading the django cache last_temperature_data
        :param request:
        :return:
        """
        cached_data = cache.get('last_temperature_data')

        if not cached_data:
            data = [{'sensor_id': 0, 'error': "Not ready"}]
            return Response(data)

        serializer = self.get_serializer(cached_data.values(), many=True)
        return Response(serializer.data)


