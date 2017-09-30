from django.contrib import admin
from tempBerry.temperatures.models import TemperatureDataEntry, Room, RoomSensorIdMapping


@admin.register(TemperatureDataEntry)
class TemperatureDataEntryAdmin(admin.ModelAdmin):
    list_display = ('sensor_id', 'created_at', 'temperature', 'humidity', 'air_pressure')
    search_fields = ('sensor_id', )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'public')
    search_fields = ('name',)


@admin.register(RoomSensorIdMapping)
class RoomSensorIdMappingAdmin(admin.ModelAdmin):
    list_display = ('room', 'sensor_id', 'start_date', 'end_date')
    search_fields = ('room', 'sensor_id')
