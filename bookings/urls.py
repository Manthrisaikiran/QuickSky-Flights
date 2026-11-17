from django.urls import path
from .views import *

urlpatterns=[
    path('book/<int:flight_id>/',book_flight,name='book_flight'),
    path('my-bookings/',my_bookings,name='my_bookings'),
    path('cancel/<int:booking_id>/',cancel_booking,name='cancel_booking'),
]