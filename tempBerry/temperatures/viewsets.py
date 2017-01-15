from temperatures.models import TemperatureDataEntry, UnknownDataEntry
from temperatures.serializers import TemperatureDataEntrySerializer
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import list_route
from rest_framework.response import Response


class TemperatureDataEntryViewSet(viewsets.ModelViewSet):
    serializer_class = TemperatureDataEntrySerializer
    queryset = TemperatureDataEntry.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('sensor_id', )

    @list_route(methods=['GET'])
    def latest(self, request):
        # get all sensor ids
        list = TemperatureDataEntry.objects.order_by('-created_at', 'sensor_id').values('created_at', 'sensor_id')[:20]

        qs = TemperatureDataEntry.objects.none()

        sensor_ids = []

        for entry in list:
            if entry['sensor_id'] in sensor_ids:
                continue
            sensor_ids.append(entry['sensor_id'])
            qs = qs | TemperatureDataEntry.objects.filter(created_at=entry['created_at'], sensor_id=entry['sensor_id'])

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
