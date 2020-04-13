from django.conf.urls import url, include
from rest_framework import routers

from tempBerry.smarthome.rest.viewsets import RoomDataViewSet

# initiate router and register all endpoints
router = routers.DefaultRouter()
router.register('rooms', RoomDataViewSet, 'rooms')

app_name = 'smarthome'

# Wire up our API with our urls
urlpatterns = [
    url(r'^', include(router.urls)),
]
