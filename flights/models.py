from django.db import models

# Create your models here.
class Flight(models.Model):
    flight_number = models.CharField(max_length=20)
    airline = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_seats = models.PositiveIntegerField(default=60)
    def __str__(self):
        return self.flight_number