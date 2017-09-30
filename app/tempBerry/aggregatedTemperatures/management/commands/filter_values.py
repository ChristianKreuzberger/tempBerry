from django.core.management.base import BaseCommand, CommandError
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

            last_datetime_date = None
            last_datetime_hour = None

            temperatures = []
            humidities = []
            entries = []

            # iterate over temperature entries
            for entry in temperature_entries:
                # extract date and hour
                datetime_date = entry.created_at.strftime('%Y-%m-%d')
                datetime_hour = entry.created_at.strftime('%H')

                if last_datetime_date and (last_datetime_date != datetime_date or last_datetime_hour != last_datetime_hour):
                    # get day + hour of the current entry
                    avg_temperature = sum(temperatures)/len(temperatures)
                    avg_humidity = sum(humidities)/len(humidities)

                    print("num_entries=", len(temperatures), ", for dates=", last_datetime_date, last_datetime_hour, avg_temperature, avg_humidity)

                    # iterate over those entries and verify that they are not too far away from avg temperature and avg humidity
                    for entry in entries:
                        if abs(entry.temperature - avg_temperature) > 5:
                            print("  The following entry seems to have a temperature outlier")
                            print("  ", entry)
                        if abs(entry.humidity - avg_humidity) > 15:
                            print("  The following entry seems to have a humidity outlier")
                            print("  ", entry)

                    entries = []
                    temperatures = []
                    humidities = []

                # add current temperature and humidity to the arrays
                temperatures.append(entry.temperature)
                humidities.append(entry.humidity)
                entries.append(entry)

                last_datetime_date = datetime_date
                last_datetime_hour = datetime_hour


