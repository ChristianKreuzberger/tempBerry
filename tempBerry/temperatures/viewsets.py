from temperatures.models import TemperatureDataEntry, UnknownDataEntry
from temperatures.serializers import TemperatureDataEntrySerializer
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


class TemperatureDataEntryViewSet(viewsets.ModelViewSet):
    serializer_class = TemperatureDataEntrySerializer
    queryset = TemperatureDataEntry.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('sensor_id', )
