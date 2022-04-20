from rest_framework import serializers
from .models import PlanesFlight, PlanesReserveplane, PlanesPlanetype

class PlaneTypeSerializer(serializers.ModelSerializer):
    remained_capacity = serializers.ReadOnlyField()
    class Meta:
        model = PlanesPlanetype
        fields = '__all__'

class ReservePlaneSerializer(serializers.ModelSerializer):
    plane_type = PlaneTypeSerializer()
    class Meta:
        model = PlanesReserveplane
        fields = '__all__'

class CarrierSerializer(serializers.ModelSerializer):
    plane_type = PlaneTypeSerializer()
    class Meta:
        model = PlanesReserveplane
        fields = '__all__'


class FlightSerializer(serializers.ModelSerializer):    
    class Meta:
        model = PlanesFlight
        fields = '__all__'
        depth=1

class FlightFilters(serializers.Serializer):
    limit = serializers.IntegerField(max_value=500, min_value=1, default=100)
    offset = serializers.IntegerField(required=False, min_value=1)
    
    airport_name = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    
    price_lower_limit = serializers.IntegerField(min_value=0, required=False)
    price_upper_limit = serializers.IntegerField(required=False)
    
    carrier_name = serializers.CharField(required=False)
    
    date = serializers.DateField(required=False)
    
