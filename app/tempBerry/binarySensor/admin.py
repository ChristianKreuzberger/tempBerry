from django.contrib import admin

from tempBerry.binarySensor.models import BinarySensorData


@admin.register(BinarySensorData)
class TemperatureDataEntryAdmin(admin.ModelAdmin):
    list_display = ('sensor_id', 'created_at', 'binary_state',)
    search_fields = ('sensor_id', )
    list_filter = ('room', 'sensor_id', )
