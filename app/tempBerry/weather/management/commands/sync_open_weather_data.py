import random
from time import sleep

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.utils import timezone

from tempBerry.smarthome.models import SmartHome
from tempBerry.weather.models import WeatherForecast

def sync_data(smarthome: SmartHome):
    pass

class Command(BaseCommand):
    help = 'Sync open weather data'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # get all smarthomes that have latitude and longitude
        smarthomes = SmartHome.objects.filter(Q(latitude__isnull=False) & Q(longitude__isnull=False))

        for smarthome in smarthomes:
            sync_data(smarthome)
