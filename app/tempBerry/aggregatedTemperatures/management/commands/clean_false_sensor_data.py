from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from tempBerry.temperatures.models import TemperatureDataEntry, Room


class Command(BaseCommand):
    help = "Cleans sensor data that are obviously wrong (e.g., negative humidity)"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # get all sensor ids
        sensor_ids = TemperatureDataEntry.objects.values('sensor_id').annotate(
            total=Count('sensor_id')
        ).order_by('total')

        for sensor_stats in sensor_ids:
            do_delete = False
            if sensor_stats['total'] < 5:
                # check if public room exists
                rooms = Room.objects.filter(sensor_id=sensor_stats['sensor_id'])
                if not rooms.exists():
                    # no rooms eixsts, we can safely delete this
                    do_delete = True
                elif not rooms.filter(public=True).exists():
                    # rooms eixsts, we need to delete the rooms but and also the data
                    rooms.delete()
                    do_delete = True

            if do_delete:
                print("deleting entries for sensor_id=", sensor_stats['sensor_id'])
                TemperatureDataEntry.objects.filter(sensor_id=sensor_stats['sensor_id']).delete()
