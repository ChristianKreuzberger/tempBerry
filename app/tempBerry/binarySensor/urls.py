from django.conf.urls import url, include
from rest_framework import routers

from tempBerry.binarySensor.rest.viewsets import BinarySensorDataViewSet

router = routers.DefaultRouter()
router.register('binary_sensors', BinarySensorDataViewSet, 'binary_sensors')

app_name = 'binarySensor'

# Wire up our API with our urls
urlpatterns = [
    url(r'^', include(router.urls)),
]
