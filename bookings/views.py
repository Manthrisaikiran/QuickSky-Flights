from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from flights.models import Flight
from .models import Booking

@login_required(login_url='login')
def book_flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)

    # Get all seats already booked with Confirmed status
    booked_seats = Booking.objects.filter(
        flight=flight,
        status='Confirmed'
    ).values_list('seat_number', flat=True)

    # Create the list of all seats
    all_seats = []

    for row in range(1, 11):
        for letter in ['A', 'B', 'C', 'D', 'E', 'F']:
            all_seats.append(str(row) + letter)

    # Remove the booked seats
    available_seats = []

    for seat in all_seats:
        if seat not in booked_seats:
            available_seats.append(seat)

    if request.method == 'POST':
        passenger_name = request.POST['passenger_name']
        seat_number = request.POST['seat_number']
        
        if seat_number not in all_seats:
            return render(request, 'booking_form.html', {
                'flight': flight,
                'available_seats': available_seats,
                'error': 'Invalid seat selected.'
            })

        # Check whether this seat is already booked
        seat_exists = Booking.objects.filter(
            flight=flight,
            seat_number=seat_number,
            status='Confirmed'
        ).exists()

        if seat_exists:
            return render(request, 'booking_form.html', {
                'flight': flight,
                'available_seats': available_seats,
                'error': 'This seat is already booked. Please select another seat.'
            })

        # Create the booking if the seat is available
        booking = Booking.objects.create(
            user=request.user,
            flight=flight,
            passenger_name=passenger_name,
            seat_number=seat_number
        )

        return render(request, 'booking_confirmation.html', {
            'booking': booking
        })
    

    return render(request, 'booking_form.html', {
        'flight': flight,
        'available_seats': available_seats
    })

@login_required(login_url='login')
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)

    return render(request, 'my_booking.html', {
        'bookings': bookings
    })

@login_required(login_url='login')
def cancel_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    if request.method == 'POST':
        booking.status = 'Cancelled'
        booking.save()

    return redirect('my_bookings')