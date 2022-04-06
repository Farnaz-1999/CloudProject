from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination

from drf_spectacular.utils import extend_schema

from .serializers import FlightSerializer, FlightFilters
from .models import Flight

class Flights(APIView):
    permission_classes = [IsAuthenticated]

    serializer_class = FlightSerializer
    pagination_class = LimitOffsetPagination

    @extend_schema(
        parameters=[FlightFilters]
    )    
    def get(self, request):
        param_serializer = FlightFilters(data=request.GET)
        param_serializer.is_valid(raise_exception=True)
        filters = param_serializer.validated_data

        queryset = Flight.objects.all().order_by('-timestamp')
        
        if filters.get('airport_name'):
            queryset = queryset.filter(
                models.Q(
                    origin_airport__name__contains=filters['airport_name']
                ) | models.Q(
                    dest_airport__name__contains=filters['airport_name']
                )
            )

        if filters.get('city'):
            queryset = queryset.filter(
                models.Q(
                    origin_airport__city__contains=filters['city']
                ) | models.Q(
                    dest_airport__city__contains=filters['city']
                )
            )

        if filters.get('price_lower_limit'):
            queryset = queryset.filter(
                price__gte=filters['price_lower_limit']
            )

        if filters.get('price_upper_limit'):
            queryset = queryset.filter(
                price__lte=filters['price_upper_limit']
            )

        if filters.get('carrier_name'):
            queryset = queryset.filter(
                carrier__name__contains=filters['carrier_name']
            )

        if filters.get('date'):
            queryset = queryset.filter(
                timestamp__date=filters['date']
            )

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, self)
        serializer = self.serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)
