from django.conf.urls import url, include
from rest_framework import routers

from tempBerry.temperatures.rest.viewsets import TemperatureDataEntryViewSet, RoomDataViewSet

# initiate router and register all endpoints
router = routers.DefaultRouter()
router.register('temperatures', TemperatureDataEntryViewSet, 'temperatures')
router.register('rooms', RoomDataViewSet, 'rooms')

app_name = 'temperatures'

# Wire up our API with our urls
urlpatterns = [
    url(r'^', include(router.urls)),
]
