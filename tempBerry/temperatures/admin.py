from django.contrib import admin
from temperatures.models import TemperatureDataEntry


@admin.register(TemperatureDataEntry)
class TemperatureDataEntryAdmin(admin.ModelAdmin):
    list_fields = ('sensor_id', 'created_at', 'temperature', 'humidity')
    search_fields = ('sensor_id', )