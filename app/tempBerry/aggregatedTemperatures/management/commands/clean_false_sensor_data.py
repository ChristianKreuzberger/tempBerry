from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from tempBerry.temperatures.models import TemperatureDataEntry, Room


class Command(BaseCommand):
    help = "Cleans sensor data that are obviously wrong (e.g., negative humidity)"

    def add_arguments(self, parser):
        pass

    def delete_data_with_less_than(self, entries=5):
        """
        Delete all temperature data entries where for a given sensor id there are less than $entries entries
        :param entries:
        :return:
        """
        # get all sensor ids and the total count of entries
        sensor_ids = TemperatureDataEntry.objects.values('sensor_id').annotate(
            total=Count('sensor_id')
        ).order_by('total')

        for sensor_stats in sensor_ids:
            do_delete = False
            if sensor_stats['total'] < entries:
                # check if public room exists
                rooms = Room.objects.filter(sensor_id_mappings__sensor_id=sensor_stats['sensor_id'])
                if not rooms.exists():
                    # no rooms exists, we can safely delete this
                    do_delete = True
                elif not rooms.filter(public=True).exists():
                    # rooms exists, we need to delete the rooms in addition to the data
                    rooms.delete()
                    do_delete = True

            if do_delete:
                print("deleting entries for sensor_id=", sensor_stats['sensor_id'])
                TemperatureDataEntry.objects.filter(sensor_id=sensor_stats['sensor_id']).delete()

    def delete_negative_humidities(self):
        """
        Deletes all entries with humidities of less than 0%
        :return:
        """
        entries = TemperatureDataEntry.objects.filter(humidity__lte=0.0)
        print("Deleting ", entries.count(), " entries with a humidity of 0.0 or less")
        entries.delete()

    def delete_very_negative_temperatures(self, threshold=-30):
        """
        Deletes all entries with temperatures of less than threshold °C (e.g., -30)
        :param threshold:
        :return:
        """
        entries = TemperatureDataEntry.objects.filter(temperature__lte=threshold)
        print("Deleting ", entries.count(), " entries with a temperature of ", threshold, "°C or less")
        entries.delete()

    def delete_very_high_temperatures(self, threshold=55):
        """
        Deletes all entries with temperatures higher than threshold °C (e.g., +55)
        :param threshold:
        :return:
        """
        entries = TemperatureDataEntry.objects.filter(temperature__gte=threshold)
        print("Deleting ", entries.count(), " entries with a temperature of ", threshold, "°C or higher")
        entries.delete()

    def handle(self, *args, **options):
        self.delete_negative_humidities()
        self.delete_very_negative_temperatures()
        self.delete_very_high_temperatures()
        self.delete_data_with_less_than(entries=5)
