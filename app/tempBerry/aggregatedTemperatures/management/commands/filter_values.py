from django.core.management.base import BaseCommand, CommandError
import numpy as np
from tempBerry.temperatures.models import TemperatureDataEntry


class Command(BaseCommand):
    help = 'Filters out outliers for each sensor'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # get all sensor ids
        sensor_ids = TemperatureDataEntry.objects.order_by('sensor_id').values('sensor_id').distinct()

        for sensor in sensor_ids:
            # get all values for a given sensor id, sorted by date
            print("Processing sensor", sensor)
            temperature_entries = TemperatureDataEntry.objects.filter(**sensor).order_by('created_at')

            last_temperature = None
            last_humidity = None
            last_date = None


            # iterate over temperature entries
            for entry in temperature_entries:
                use_current_value = True

                if last_date and (entry.created_at - last_date).seconds/60 < 5:
                    # last value was within 5 minutes
                    # check how much temperature and or humidity have changed
                    if entry.temperature and last_temperature and abs(entry.temperature - last_temperature) > 5:
                        print("Temperature changed too much with the following entry", entry)
                        print("Last temperature was: ", last_temperature)
                        use_current_value = False
                    if entry.humidity and last_humidity and abs(entry.humidity - last_humidity) > 10:
                        print("Humidity changed too much with the following entry", entry)
                        print("Last humidity was: ", last_humidity)
                        use_current_value = False

                if use_current_value:
                    last_temperature = entry.temperature
                    last_humidity = entry.humidity
                    last_date = entry.created_at
                else:
                    print("Should probably delete it...")


