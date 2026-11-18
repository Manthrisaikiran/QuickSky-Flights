# from django.shortcuts import render
# from .models import Flight

# def home(request):
#     flights = []
    
#     source = request.GET.get('source')
#     destination = request.GET.get('destination')
#     date = request.GET.get('date')

#     if source and destination and date:
#         flights = Flight.objects.filter(
#             source__iexact=source,
#             destination__iexact=destination,
#             departure_time__date=date
#         )

#     for flight in flights:
#         duration = flight.arrival_time - flight.departure_time
#         total_minutes = int(duration.total_seconds() // 60)

#         hours = total_minutes // 60
#         minutes = total_minutes % 60

#         flight.duration = f"{hours}h {minutes}m"

#     return render(request, 'home.html', {
#         'flights': flights,
#         'source': source,
#         'destination': destination,
#         'date': date
#     })


# ...............................................................................................



from functools import wraps

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from .models import Flight
from .forms import FlightForm


# ==========================================
# ADMIN PERMISSION DECORATOR
# ==========================================

def admin_required(view_func):

    @wraps(view_func)
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):

        # Check whether user is admin/staff
        if not request.user.is_staff:
            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return wrapper


# ==========================================
# HOMEPAGE AND FLIGHT SEARCH
# ==========================================

def home(request):

    flights = []

    source = request.GET.get('source')
    destination = request.GET.get('destination')
    date = request.GET.get('date')

    if source and destination and date:

        flights = Flight.objects.filter(
            source__iexact=source,
            destination__iexact=destination,
            departure_time__date=date
        )

    for flight in flights:

        duration = flight.arrival_time - flight.departure_time

        total_minutes = int(duration.total_seconds() // 60)

        hours = total_minutes // 60
        minutes = total_minutes % 60

        flight.duration = f"{hours}h {minutes}m"

    return render(request, 'home.html', {
        'flights': flights,
        'source': source,
        'destination': destination,
        'date': date
    })


# ==========================================
# ADMIN: DISPLAY ALL FLIGHTS
# ==========================================

@admin_required
def manage_flights(request):

    flights = Flight.objects.all().order_by('-id')

    return render(request, 'flights/manage_flights.html', {
        'flights': flights
    })


# ==========================================
# ADMIN: ADD NEW FLIGHT
# ==========================================

@admin_required
def add_flight(request):

    if request.method == 'POST':

        form = FlightForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Flight added successfully!'
            )

            return redirect('manage_flights')

    else:

        form = FlightForm()

    return render(request, 'flights/flight_form.html', {
        'form': form,
        'title': 'Add New Flight'
    })


# ==========================================
# ADMIN: EDIT EXISTING FLIGHT
# ==========================================

@admin_required
def edit_flight(request, flight_id):

    flight = get_object_or_404(Flight, id=flight_id)

    if request.method == 'POST':

        form = FlightForm(
            request.POST,
            instance=flight
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Flight updated successfully!'
            )

            return redirect('manage_flights')

    else:

        form = FlightForm(instance=flight)

    return render(request, 'flights/flight_form.html', {
        'form': form,
        'title': 'Edit Flight'
    })


# ==========================================
# ADMIN: DELETE FLIGHT
# ==========================================

@admin_required
def delete_flight(request, flight_id):

    flight = get_object_or_404(Flight, id=flight_id)

    if request.method == 'POST':

        flight.delete()

        messages.success(
            request,
            'Flight deleted successfully!'
        )

        return redirect('manage_flights')

    return render(request, 'flights/confirm_delete.html', {
        'flight': flight
    })
