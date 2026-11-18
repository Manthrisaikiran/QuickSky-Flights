# from django.contrib import admin
# from .models import *
# # Register your models here.

# admin.site.register(Flight)

from django.contrib import admin
from .models import Flight


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'flight_number',
        'airline',
        'source',
        'destination',
        'departure_time',
        'arrival_time',
        'price',
        'total_seats',
    )

    search_fields = (
        'flight_number',
        'airline',
        'source',
        'destination',
    )

    list_filter = (
        'airline',
        'source',
        'destination',
    )

    ordering = ('departure_time',)

    list_per_page = 20
