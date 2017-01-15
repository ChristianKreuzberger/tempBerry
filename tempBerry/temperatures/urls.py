from rest_framework import routers
from django.conf.urls import url, include
from temperatures.viewsets import TemperatureDataEntryViewSet

# initiate router and register all endpoints
router = routers.DefaultRouter()
router.register('temperatures', TemperatureDataEntryViewSet, 'temperatures')

# Wire up our API with our urls
urlpatterns = [
    url(r'^', include(router.urls)),
]