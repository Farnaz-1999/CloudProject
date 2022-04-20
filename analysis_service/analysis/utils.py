from sqlite3 import SQLITE_CREATE_TRIGGER
from django.utils import timezone
from django.db import models

from dateutil.relativedelta import relativedelta

from rest_framework.exceptions import NotFound

# from analysis.models import Carrier, PlaneType

from .models import PlanesFlight, PlanesAirport, PlanesPlanetype, PlanesReserveplane

def traffic(airport_name: str, date_start: timezone.datetime, date_end: timezone.datetime) -> dict:
    try:
        airport = PlanesAirport.objects.using('flight_db').get(
            name=airport_name
        )
    except PlanesAirport.DoesNotExist:
        raise NotFound

    data = []
    start_month = timezone.datetime(year=date_start.year, month=date_start.month, day=1)
    end_month = timezone.datetime(year=date_end.year, month=date_end.month, day=1)

    while start_month <= end_month:
        data.append({
            'city': airport.city,
            'city_input': PlanesFlight.objects.using('flight_db').filter(
                dest_airport__city=airport.city,
                timestamp__year=start_month.year,
                timestamp__month=start_month.month,
            ).count(),
            'city_output': PlanesFlight.objects.using('flight_db').filter(
                origin_airport__city=airport.city,
                timestamp__year=start_month.year,
                timestamp__month=start_month.month,
            ).count(),
            'airport_input': PlanesFlight.objects.using('flight_db').filter(
                dest_airport=airport,
                timestamp__year=start_month.year,
                timestamp__month=start_month.month,
            ).count(),
            'airport_output': PlanesFlight.objects.using('flight_db').filter(
                origin_airport=airport,
                timestamp__year=start_month.year,
                timestamp__month=start_month.month,
            ).count(),
            'date': str(start_month),
        })
        start_month = start_month + relativedelta(months=1)

    return data

def sale(carrier_name: str, date_start: timezone.datetime, date_end: timezone.datetime) -> dict:
    data = []
    start_month = timezone.datetime(year=date_start.year, month=date_start.month, day=1)
    end_month = timezone.datetime(year=date_end.year, month=date_end.month, day=1)

    while start_month <= end_month:
        data.append({
            'carrier': carrier_name,
            'total': (PlanesFlight.objects.using('flight_db').filter(
                            carrier__name=carrier_name,
                            timestamp__year=start_month.year,
                            timestamp__month=start_month.month,
                        )
                        .aggregate(
                            total=models.Sum('price', field="price*plane_type.capacity")
                        )['total']
            ),
            'date': str(start_month)
        })
        start_month = start_month + relativedelta(months=1)
    return data

def flights(airplane_name: str, date_start: timezone.datetime, date_end: timezone.datetime) -> dict:
    data = []
    start_month = timezone.datetime(year=date_start.year, month=date_start.month, day=1)
    end_month = timezone.datetime(year=date_end.year, month=date_end.month, day=1)

    while start_month <= end_month:
        data.append({
            'plane': airplane_name,
            'flights': PlanesFlight.objects.using('flight_db').filter(
                plane_type__name=airplane_name,
                timestamp__year=start_month.year,
                timestamp__month=start_month.month,
            ).count(),
            'date': str(start_month),
        })
        start_month = start_month + relativedelta(months=1)

    return data

def test_query():
    """
        query for counting each flight reserves
    """

    q = PlanesFlight.objects.using('flight_db').annotate(
        reserve_count=models.Count('reserves')
    ).all()
    f = q.get(pk=4567)
    print(f.reserve_count)
    print(q)
