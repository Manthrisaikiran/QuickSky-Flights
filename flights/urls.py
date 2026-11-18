# from django.urls import path
# from .views import *

# urlpatterns = [
#     path('',home,name='home'),
# ]


# .............................................


from django.urls import path
from .views import (
    home,
    manage_flights,
    add_flight,
    edit_flight,
    delete_flight,
)

urlpatterns = [
    path('', home, name='home'),

    path('manage-flights/', manage_flights, name='manage_flights'),

    path('manage-flights/add/', add_flight, name='add_flight'),

    path('manage-flights/edit/<int:flight_id>/', edit_flight, name='edit_flight'),

    path('manage-flights/delete/<int:flight_id>/', delete_flight, name='delete_flight'),
]
