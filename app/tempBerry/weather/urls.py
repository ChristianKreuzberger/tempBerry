from django.conf.urls import url, include
from rest_framework import routers

# initiate router and register all endpoints
router = routers.DefaultRouter()

app_name = 'weather'

# Wire up our API with our urls
urlpatterns = [
    url(r'^', include(router.urls)),
]
