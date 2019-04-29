from datetime import timedelta

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from tempBerry.binarySensor.models import BinarySensorData
from tempBerry.binarySensor.rest.serializers import BinarySensorDataSerializer

__all__ = [
    'BinarySensorDataViewSet'
]


class BinarySensorDataViewSet(viewsets.ModelViewSet):
    """
    Viewset for binary sensor data
    """
    serializer_class = BinarySensorDataSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('room_id', 'sensor_id', )

    def get_queryset(self):
        end_date = timezone.now()
        start_date = end_date - timedelta(hours=96)
        return BinarySensorData.objects.filter(
            created_at__range=(start_date, end_date)
        ).order_by('created_at')
