from rest_framework import routers
from django.conf.urls import url, include
from tempBerry.temperatures.viewsets import TemperatureDataEntryViewSet, RoomDataViewSet

# initiate router and register all endpoints
router = routers.DefaultRouter()
router.register('temperatures', TemperatureDataEntryViewSet, 'temperatures')
router.register('rooms', RoomDataViewSet, 'rooms')

# Wire up our API with our urls
urlpatterns = [
    url(r'^', include(router.urls)),
]