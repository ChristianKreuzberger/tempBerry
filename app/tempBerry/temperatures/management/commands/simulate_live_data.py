import random
from time import sleep

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.utils import timezone

from tempBerry.temperatures.models import TemperatureDataEntry, RoomSensorIdMapping


class Command(BaseCommand):
    help = 'Simulate Live Data for all sensor ids'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # get all sensor ids
        sensor_ids = RoomSensorIdMapping.objects.order_by('sensor_id').filter()

        now = timezone.now()

        # get all active sensor ids
        sensor_ids = RoomSensorIdMapping.objects.filter(
            Q(start_date__lte=now, end_date__gte=now) | Q(start_date__lte=now, end_date__isnull=True)
        ).values_list('sensor_id', flat=True)

        time_between = 60  # seconds

        sleep_time = time_between / len(sensor_ids)

        base_temp = 21
        base_hum = 50

        while True:
            # iterate over all sensors
            for sensor_id in sensor_ids:
                print(sensor_id)

                temperature = base_temp + random.randint(0, 20) / 10.0
                humidity = base_hum + random.randint(0, 100) / 5.0

                TemperatureDataEntry.objects.create(
                    sensor_id=sensor_id,
                    temperature=temperature,
                    humidity=humidity,
                    battery=0
                )

                sleep(sleep_time)
