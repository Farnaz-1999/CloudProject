# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class PlanesAirport(models.Model):
    name = models.CharField(unique=True, max_length=64)
    city = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'planes_airport'


class PlanesCarrier(models.Model):
    name = models.CharField(unique=True, max_length=64)
    rating = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'planes_carrier'


class PlanesFlight(models.Model):
    timestamp = models.DateTimeField()
    sit_class = models.CharField(max_length=16)
    price = models.PositiveIntegerField()
    carrier = models.ForeignKey(PlanesCarrier, models.DO_NOTHING)
    dest_airport = models.ForeignKey(PlanesAirport, models.DO_NOTHING, related_name='input_flights')
    origin_airport = models.ForeignKey(PlanesAirport, models.DO_NOTHING, related_name='output_flights')
    plane_type = models.ForeignKey('PlanesPlanetype', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'planes_flight'


class PlanesPlanetype(models.Model):
    name = models.CharField(unique=True, max_length=64)
    capacity = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'planes_planetype'


class PlanesReserveplane(models.Model):
    user_id = models.CharField(max_length=128)
    flight = models.ForeignKey(PlanesFlight, models.DO_NOTHING, blank=True, null=True, related_name='reserves')

    class Meta:
        managed = False
        db_table = 'planes_reserveplane'
