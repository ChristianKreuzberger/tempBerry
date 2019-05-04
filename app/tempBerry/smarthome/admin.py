from django.contrib import admin
from tempBerry.smarthome.models import SmartHome, SmartHomeApiKey, Room


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
