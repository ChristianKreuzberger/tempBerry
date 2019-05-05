from django.contrib import admin
from tempBerry.smarthome.models import SmartHome, SmartHomeApiKey, Room, Sensor, SensorIdToSensorMapping


@admin.register(SmartHome)
class SmartHomeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at', )


@admin.register(SmartHomeApiKey)
class SmartHomeApiKeyAdmin(admin.ModelAdmin):
    list_filter = ('smarthome', )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'last_updated_at', 'public')
    search_fields = ('name',)
    list_filter = ('public', )


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'last_updated_at', 'public')
    search_fields = ('name', 'type', )
    list_filter = ('public', 'type',)


@admin.register(SensorIdToSensorMapping)
class SensorIdToSensorMappingAdmin(admin.ModelAdmin):
    list_display = ('real_sensor', 'sensor_id', 'start_date', 'end_date')
    search_fields = ('real_sensor', 'sensor_id')
