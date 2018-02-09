from django.contrib import admin
from tempBerry.aggregatedTemperatures.models import HourlyAggregatedTemperature


@admin.register(HourlyAggregatedTemperature)
class HourlyAggregatedTemperatureAdmin(admin.ModelAdmin):
    list_display = ('room', 'datetime_day', 'datetime_hour', 'average_temperature', 'average_humidity',)
    search_fields = ('room', 'datetime_day')
    list_filter = ('room',)
