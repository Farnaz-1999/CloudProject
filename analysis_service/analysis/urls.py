from django.urls import path

from . import views

urlpatterns = [
    # path('flights/', views.Flights.as_view()),
    # path('reserves/<int:pk>/', views.DeleteReserve.as_view()),
    # path('reserves/<str:plane_type>/', views.ReservePlaneAPI.as_view()),
    path('analysis/<str:time_start>/<str:time_end>/<str:airport_name1>/<str:airport_name2>', views.TrafficAnalysis.as_view()),
    path('reserves/<str:time_start>/<str:time_end>/<str:carrier_name1>/<str:carrier_name2>', views.CarrierAnalysis.as_view()),
    path('analysis/flights/<str:time_start>/<str:time_end>/<str:airplane_name1>/<str:airplane_name2>', views.FlightAnalysis.as_view()),
    # path('reserves/', views.ListReserves.as_view())
]
