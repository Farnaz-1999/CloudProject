from rest_framework import serializers
from .models import Flight

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
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
    
