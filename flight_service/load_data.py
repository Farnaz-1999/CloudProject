import os
from time import time
import django
import pandas as pd

from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flight_service.settings')
django.setup()

from planes.models import Flight, PlaneType, Carrier, Airport

if __name__ == '__main__':
    print('Loading planes data...')
    planes = pd.read_csv(os.path.join('data', 'planes.csv'))

    for index, row in planes.iterrows():
        try:
            PlaneType.objects.get(
                name=row[0]
            )
        except PlaneType.DoesNotExist:
            PlaneType.objects.create(
                name=row[0],
                capacity=row[1]
            )

    print('Loading airports data...')
    airports = pd.read_csv(os.path.join('data', 'airports.csv'))

    for index, row in airports.iterrows():
        try:
            Airport.objects.get(
                name=row[1]
            )
        except Airport.DoesNotExist:
            Airport.objects.create(
                name=row[1],
                city=row[0]
            )
    
    print('Loading carriers data...')
    carriers = pd.read_csv(os.path.join('data', 'carriers.csv'))

    for index, row in carriers.iterrows():
        try:
            Carrier.objects.get(
                name=row[0]
            )
        except Carrier.DoesNotExist:
            Carrier.objects.create(
                name=row[0],
                rating=row[1]
            )

    print('Loading flights data...')
    flights = pd.read_csv(os.path.join('data', 'flights.csv'))

    for index, row in flights.iterrows():
        try:
            origin_airport = Airport.objects.get(
                name=row['origin_airport']
            )
            dest_airport = Airport.objects.get(
                name=row['dest_airport']
            )
            carrier = Carrier.objects.get(
                name=row['carrier']
            )
            plane_type = PlaneType.objects.get(
                name=row['plane_type']
            )
            # 2021-11-06 20:00
            timestamp = timezone.datetime.fromisoformat(
                row['datetime']
            )
            if timezone.is_naive(timestamp):
                timestamp = timezone.make_aware(timestamp)

            Flight.objects.get(
                origin_airport=origin_airport,
                dest_airport=dest_airport,
                timestamp=timestamp,
                carrier=carrier,
                sit_class=row['class'],
                plane_type=plane_type
            )
        except Flight.DoesNotExist:
            Flight.objects.create(
                origin_airport=origin_airport,
                dest_airport=dest_airport,
                timestamp=timestamp,
                carrier=carrier,
                sit_class=row['class'],
                plane_type=plane_type
            )

    print('Finished loading data')
