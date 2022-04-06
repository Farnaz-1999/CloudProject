from django.db import models

class PlaneType(models.Model):
    name = models.CharField(max_length=64, unique=True)
    capacity = models.PositiveIntegerField()

    @property
    def remained_capacity(self, ):
        return self.get_remained_capacity()
        
    def get_remained_capacity(self, ):
        return self.capacity - (ReservePlane.objects.filter(plane_type=self).count() or 0)

class ReservePlane(models.Model):
    plane_type = models.ForeignKey(
        PlaneType, on_delete=models.CASCADE, related_name='reserves'
    )
    user_id = models.CharField(max_length=128)

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
