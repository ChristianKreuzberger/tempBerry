from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from tempBerry.aggregatedTemperatures.models import HourlyAggregatedTemperature
from tempBerry.smarthome.models import Room
from tempBerry.temperatures.models import TemperatureDataEntry


class Command(BaseCommand):
    help = 'Updates the average values in aggregatedTemperatures'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # get all rooms that we need to process
        rooms = Room.objects.filter(public=True)

        print("Processing {num} rooms".format(num=len(rooms)))

        for room in rooms:
            # get the latest HourlyAggregatedTemperature for the given room
            last_aggregated_entry = HourlyAggregatedTemperature.objects.filter(room=room).order_by(
                '-datetime_day', '-datetime_hour'
            ).first()

            # check if an entry exists
            if not last_aggregated_entry:
                # no entry exists, just aggregate all data
                date_time_start = timezone.datetime(2000, 1, 1, tzinfo=timezone.get_current_timezone())
            else:
                # start with the same day
                date_time_start = last_aggregated_entry.datetime_day

            # get all values for a given room, sorted by date, starting with date_time_start
            temperature_entries = TemperatureDataEntry.objects.filter(
                room=room, created_at__gte=date_time_start
            ).order_by('created_at')

            print("Processing room {room} with {num} temperature entries".format(
                room=str(room), num=len(temperature_entries))
            )

            last_datetime_date = None
            last_datetime_hour = None

            temperatures = []
            humidities = []

            # iterate over temperature entries
            for entry in temperature_entries:
                # extract date and hour
                datetime_date = entry.created_at.strftime('%Y-%m-%d')
                datetime_hour = entry.created_at.strftime('%H')

                # if date and or the hour have changed
                if last_datetime_date and \
                        (last_datetime_date != datetime_date or last_datetime_hour != datetime_hour):
                    # calculate average temperature and humidity
                    avg_temperature = sum(temperatures)/len(temperatures)
                    avg_humidity = sum(humidities)/len(humidities)

                    print(last_datetime_date, last_datetime_hour, avg_temperature, avg_humidity)

                    # add this to database
                    HourlyAggregatedTemperature.objects.update_or_create(
                        room=room,
                        datetime_day=last_datetime_date,
                        datetime_hour=last_datetime_hour,
                        average_temperature=avg_temperature,
                        average_humidity=avg_humidity
                    )

                    # reset temperatures and humidities array
                    temperatures = []
                    humidities = []

                # add current temperature and humidity to the arrays
                temperatures.append(entry.temperature)
                humidities.append(entry.humidity)

                last_datetime_date = datetime_date
                last_datetime_hour = datetime_hour


