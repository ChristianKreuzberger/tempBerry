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


class RoomDataViewSet(viewsets.ModelViewSet):
    """
    Viewset for room
    """
    serializer_class = RoomSerializer
    filter_backends = (DjangoFilterBackend,)
    queryset = Room.objects.all()

    def get_queryset(self, *args, **kwargs):
        return Room.objects.filter(
            public=True
        ).prefetch_related('smarthome', 'sensors')

    @action(detail=False, methods=['GET'])
    def latest(self, request):
        """
        Display latest data by reading the django cache last_sensor_data
        :param request:
        :return:
        """
        cached_data = cache.get('last_sensor_data')
        if not cached_data:
            cached_data = dict()

        # get queryset with public rooms only
        rooms = self.get_queryset()

        print(cached_data)

        # for each room, check if there are data in cached_data
        for room in rooms:
            live_data = []
            # get all live data based on the sensors of the room
            for sensor in room.sensors.all():
                cached_entry = cached_data.get(sensor.id, None)
                if cached_entry:
                    live_data.append(cached_entry)

            room.live_data = live_data

        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)
