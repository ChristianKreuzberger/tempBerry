from django.contrib import admin
from tempBerry.weather.models import WeatherForecast


@admin.register(WeatherForecast)
class WeatherForecastAdmin(admin.ModelAdmin):
    list_display = ('source', 'created_at', 'smarthome')
    list_filters = ('smarthome', )
