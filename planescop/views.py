from datetime import datetime
import matplotlib.pyplot as plt

from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework import status

from drf_spectacular.utils import extend_schema

from .serializers import FlightSerializer, FlightFilters, ReservePlaneSerializer
from .models import Airport, Flight, PlaneType, ReservePlane
from ..analysis import utils

class ReservePlaneAPI(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReservePlaneSerializer

    @extend_schema(
        request=None
    )
    def post(self, request, time_start, time_end, airport_name1, airport_name2):
        dt_S = datetime.strptime(time_start, '%Y-%m-%d')
        dt_E = datetime.strptime(time_end, '%Y-%m-%d')
        A1Data=utils.traffic(airport_name1,dt_S,dt_E)
        A2Data=utils.traffic(airport_name2,dt_S,dt_E)

        # data for plotting
        x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        y = [5, 7, 8, 1, 4, 9, 6, 3, 5, 2, 1, 8]
        
        plt.plot(x, y)
        
        plt.xlabel('x-axis label')
        plt.ylabel('y-axis label')
        plt.title('Matplotlib Example')
        
        plt.savefig("output.jpg")

        # return Response(
        #     self.serializer_class(reserved).data,
        #     status=status.HTTP_201_CREATED
        # )
    
class DeleteReserve(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReservePlaneSerializer

    def delete(self, request, pk):
        try:
            reserved = ReservePlane.objects.get(pk=pk)
        except ReservePlane.DoesNotExist:
            raise NotFound
        reserved.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ListReserves(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReservePlaneSerializer

    def get(self, request):
        queryset = ReservePlane.objects.filter(
            user_id=request.user.id
        )
        serializer = self.serializer_class(
            queryset, many=True
        )
        return Response(serializer.data)

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
