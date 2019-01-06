from django.contrib import admin
from tempBerry.smarthome.models import SmartHome, SmartHomeApiKey


@admin.register(SmartHome)
class SmartHomeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at', )


@admin.register(SmartHomeApiKey)
class RoomAdmin(admin.ModelAdmin):
    list_filter = ('smarthome', )
