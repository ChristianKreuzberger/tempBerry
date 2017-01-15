from temperatures.models import TemperatureDataEntry, UnknownDataEntry
from temperatures.serializers import TemperatureDataEntrySerializer
from rest_framework import viewsets


class TemperatureDataEntryViewSet(viewsets.ModelViewSet):
    serializer_class = TemperatureDataEntrySerializer
    queryset = TemperatureDataEntry.objects.all()