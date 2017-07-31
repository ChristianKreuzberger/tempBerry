from django.contrib import admin
from temperatures.models import TemperatureDataEntry, Room


@admin.register(TemperatureDataEntry)
class TemperatureDataEntryAdmin(admin.ModelAdmin):
    list_display = ('sensor_id', 'created_at', 'temperature', 'humidity')
    search_fields = ('sensor_id', )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'sensor_id', 'created_at')
    search_fields = ('name', 'sensor_id')
