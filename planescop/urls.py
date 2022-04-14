from django.urls import path

from . import views

urlpatterns = [
    path('flights/', views.Flights.as_view()),
    path('reserves/<int:pk>/', views.DeleteReserve.as_view()),
    # path('reserves/<str:plane_type>/', views.ReservePlaneAPI.as_view()),
    path('reserves/<str:time_start>/<str:time_end>/<str:airport_name1>/<str:airport_name2>', views.ReservePlaneAPI.as_view()),
    path('reserves/', views.ListReserves.as_view())
]
