from django.db import models

class PlaneType(models.Model):
    name = models.CharField(max_length=64, unique=True)
    capacity = models.PositiveIntegerField()

class Carrier(models.Model):
    name = models.CharField(max_length=64, unique=True)
    rating = models.PositiveIntegerField()

class Airport(models.Model):
    name = models.CharField(max_length=64, unique=True)
    city = models.CharField(max_length=128)

class Flight(models.Model):
    origin_airport = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name='out_flights'
    )
    dest_airport = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name='in_flights'
    )
    timestamp = models.DateTimeField()
    carrier = models.ForeignKey(
        Carrier, on_delete=models.CASCADE, related_name='flights'
    )
    sit_class = models.CharField(max_length=16)
    plane_type = models.ForeignKey(
        PlaneType, on_delete=models.CASCADE, related_name='flights'
    )
    price = models.PositiveIntegerField()
