from django.urls import path

from . import views

urlpatterns = [
    path('flights/', views.Flights.as_view()),
    path('reserves/<int:pk>/', views.DeleteReserve.as_view()),
    path('reserves/', views.ReservesView.as_view()),
]
