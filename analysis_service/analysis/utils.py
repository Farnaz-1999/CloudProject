from calendar import month
from django.utils import timezone

from rest_framework.exceptions import NotFound

from .models import PlanesFlight, PlanesAirport

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
            'airport': airport.name,
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
        start_month = timezone.datetime(
            year=start_month.year,
            month=(start_month.month+1)%12,
            day=1,
        )
    return data
