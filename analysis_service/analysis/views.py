from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

from django.http import HttpResponse, HttpResponseRedirect
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
from .utils import flights, traffic, sale

class TrafficAnalysis(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReservePlaneSerializer

    @extend_schema(
        request=None
    )
    def post(self, request, time_start, time_end, airport_name1, airport_name2):
        dt_S = datetime.strptime(time_start, '%Y-%m-%d')
        dt_E = datetime.strptime(time_end, '%Y-%m-%d')
        A1Data=traffic(airport_name1,dt_S,dt_E)
        A2Data=traffic(airport_name2,dt_S,dt_E)

        if(len(A1Data)!=[] and len(A2Data)!=[]):
            bars_Title = ["CIn", "COut", "AIn", "AOut"]
            bars=[]
            data1 = []
            data2 = []

            for j in range(len(A1Data)):
                for i in range(1,5):
                    bars.append(bars_Title[i-1]+"-"+str(j))
                    data1.append(list(A1Data[j].values())[i])
                    data2.append(list(A2Data[j].values())[i])

            x_axis = np.arange(len(bars))
            plt.bar(x_axis -0.2, data1, width=0.4, color='yellow', label=airport_name1+"-"+A1Data[0]['city'])
            plt.bar(x_axis +0.2, data2, width=0.4, color='red', label=airport_name2+"-"+A2Data[0]['city'])
            plt.xticks(x_axis,bars)
            plt.legend()
            plt.savefig("./media/output.jpg")

            return HttpResponseRedirect(redirect_to="http://127.0.0.1:8000/media/output.jpg")
        else:
            return HttpResponse("No data in this time range!!!")

class CarrierAnalysis(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReservePlaneSerializer
    
    @extend_schema(
        request=None
    )
    def post(self, request, time_start, time_end, carrier_name1, carrier_name2):
        dt_S = datetime.strptime(time_start, '%Y-%m-%d')
        dt_E = datetime.strptime(time_end, '%Y-%m-%d')
        A1Data=sale(carrier_name1,dt_S,dt_E)
        A2Data=sale(carrier_name2,dt_S,dt_E)

        print(A1Data)
        print(A2Data)

        # if(len(A1Data)!=[] and len(A2Data)!=[]):
        #     bars=[]
        #     data1 = []
        #     data2 = []

        #     for j in range(len(A1Data)):
        #         bars.append(j)
        #         //data1.append(A1Data[j]['total'])
        #         //data2.append(A2Data[j]['total'])

        #     x_axis = np.arange(len(bars))
        #     plt.bar(x_axis -0.2, data1, width=0.4, color='yellow', label=carrier_name1)
        #     plt.bar(x_axis +0.2, data2, width=0.4, color='red', label=carrier_name2)
        #     plt.xticks(x_axis,bars)
        #     plt.legend()
        #     plt.savefig("./media/coutput.jpg")

        #     return HttpResponseRedirect(redirect_to="http://127.0.0.1:8000/media/coutput.jpg")
        # else:
        return HttpResponse("No data in this time range!!!")

class FlightAnalysis(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReservePlaneSerializer

    @extend_schema(
        request=None
    )
    def post(self, request, time_start, time_end, airplane_name1, airplane_name2):
        dt_S = datetime.strptime(time_start, '%Y-%m-%d')
        dt_E = datetime.strptime(time_end, '%Y-%m-%d')
        A1Data=flights(airplane_name1,dt_S,dt_E)
        A2Data=flights(airplane_name2,dt_S,dt_E)

        if(len(A1Data)!=[] and len(A2Data)!=[]):
            bars=[]
            data1 = []
            data2 = []

            for j in range(len(A1Data)):
                bars.append(j)
                data1.append(A1Data[j]['flights'])
                data2.append(A2Data[j]['flights'])

            x_axis = np.arange(len(bars))
            plt.bar(x_axis -0.2, data1, width=0.4, color='yellow', label=airplane_name1)
            plt.bar(x_axis +0.2, data2, width=0.4, color='red', label=airplane_name2)
            plt.xticks(x_axis,bars)
            plt.legend()
            plt.savefig("./media/foutput.jpg")

            return HttpResponseRedirect(redirect_to="http://127.0.0.1:8000/media/foutput.jpg")
        else:
            return HttpResponse("No data in this time range!!!")

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
