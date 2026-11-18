
from django import forms
from .models import Flight


class FlightForm(forms.ModelForm):

    class Meta:
        model = Flight

        fields = [
            'flight_number',
            'airline',
            'source',
            'destination',
            'departure_time',
            'arrival_time',
            'price',
            'total_seats'
        ]

        widgets = {
            'departure_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),

            'arrival_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['departure_time'].input_formats = [
            '%Y-%m-%dT%H:%M'
        ]

        self.fields['arrival_time'].input_formats = [
            '%Y-%m-%dT%H:%M'
        ]
