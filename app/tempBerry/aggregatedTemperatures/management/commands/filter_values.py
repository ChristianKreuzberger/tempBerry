from django.core.management.base import BaseCommand, CommandError
import numpy as np
import scipy as sp
from scipy import stats
from tempBerry.temperatures.models import TemperatureDataEntry


def mean_confidence_interval(data, confidence=0.95):
    mean, sigma, median = np.mean(data), np.std(data), np.median(data)
    interval = stats.norm.interval(0.95, loc=mean, scale=sigma)

    return {
        'mean': mean,
        'median': median,
        'min': interval[0],
        'max': interval[1]
    }


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
            entries_to_check = []

            # iterate over temperature entries
            for entry in temperature_entries:
                # extract date and hour of the current entry
                datetime_date = entry.created_at.strftime('%Y-%m-%d')
                datetime_hour = entry.created_at.strftime('%H')

                if last_datetime_date and (last_datetime_date != datetime_date or last_datetime_hour != datetime_hour):
                    # date and/or hour have changed!
                    avg_temperature = sum(temperatures)/len(temperatures)
                    avg_humidity = sum(humidities)/len(humidities)

                    # Calculate 95% confidence interval for temp and humidity
                    confidence_temperature = mean_confidence_interval(temperatures, 0.99)
                    confidence_humidity = mean_confidence_interval(humidities, 0.99)

                    print(confidence_temperature)
                    print(confidence_humidity)

                    print("Checking outliers for {} {}".format(last_datetime_date, last_datetime_hour))

                    # iterate over those entries and verify that they are not too far away from avg temperature and avg humidity
                    print("Humidity and temperature outliers (avg_temp={}, avg_hum={}):".format(avg_temperature, avg_humidity))
                    for special_entry in entries_to_check:
                        # detect temperature diffs greater than 10 °C within one hour
                        if special_entry.temperature and \
                                (special_entry.temperature < confidence_temperature['min'] or special_entry.temperature > confidence_temperature['max']):
                            print("  T ", special_entry)
                        if special_entry.humidity and \
                                (special_entry.humidity < confidence_humidity['min'] or special_entry.humidity > confidence_humidity['max']):
                            print("  H ", special_entry)


                    entries_to_check = []
                    temperatures = []
                    humidities = []

                # add current temperature and humidity to the arrays
                if entry.temperature:
                    temperatures.append(entry.temperature)
                if entry.humidity:
                    humidities.append(entry.humidity)
                entries_to_check.append(entry)

                last_datetime_date = datetime_date
                last_datetime_hour = datetime_hour


