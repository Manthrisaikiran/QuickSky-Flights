from django.shortcuts import render
from .models import Flight

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
