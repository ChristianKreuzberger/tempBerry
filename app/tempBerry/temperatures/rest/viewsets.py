from datetime import timedelta

from django.core.cache import cache
from django.db.models import Avg, Max, Min, Count
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response

from tempBerry.temperatures.models import TemperatureDataEntry, Room
from tempBerry.temperatures.rest.serializers import TemperatureDataEntrySerializer, RoomSerializer, \
    RoomLiveDataSerializer


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
            max_humidity=Max('humidity'),
            min_humidity=Min('humidity'),
            avg_humidity=Avg('humidity'),
        )


class RoomDataViewSet(viewsets.ModelViewSet):
    """
    Viewset for room
    """
    serializer_class = RoomSerializer
    filter_backends = (DjangoFilterBackend,)
    queryset = Room.objects.all()

    @list_route(methods=['GET'])
    def new_rooms(self, request):
        """
        Returns rooms that are not public, but have a lot of data
        :param request:
        :return:
        """
        # get all sensor IDs that have at least 10 entries
        sensor_ids = TemperatureDataEntry.objects.values('sensor_id').annotate(
            total=Count('sensor_id')
        ).order_by('total').filter(total__gte=10).values_list('sensor_id', flat=True)

        # get all rooms that are not public
        rooms = self.get_queryset().filter(public=False, sensor_id__in=sensor_ids)

        serializer = self.get_serializer(rooms, many=True)

        return Response(serializer.data)

    @list_route(methods=['GET'])
    def latest(self, request):
        """
        Display latest data by reading the django cache last_temperature_data
        :param request:
        :return:
        """
        cached_data = cache.get('last_temperature_data')

        # get queryset with public rooms only
        rooms = self.get_queryset().filter(public=True)

        if not cached_data:
            # no cached_data available yet, fill it
            cached_data = {}
            for room in rooms:
                data_set = room.temperaturedataentry_set.latest('created_at')
                if data_set:
                    cached_data[room.id] = data_set
            cache.set('last_temperature_data', cached_data)

        # for each room, check if there are data in cached_data
        for room in rooms:
            room.live_data = cached_data.get(room.id, None)

        serializer = RoomLiveDataSerializer(rooms, many=True)
        return Response(serializer.data)

    @detail_route(methods=['GET'])
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

    @detail_route(methods=['GET'])
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
        )

        return Response(qs)

    @detail_route(methods=['GET'])
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
        )

        return Response(qs)