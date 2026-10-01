from django.db import models
from django.contrib.auth.models import AbstractUser
from app import choices
from django.core.exceptions import ValidationError

# Create your models here.
class CustomUser(AbstractUser):
    role=models.CharField(max_length=2,choices=choices.UserRole.choices,default='C')
    phone_number=models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.username



class Bus(models.Model):
    bus_model=models.CharField(max_length=255)
    bus_number=models.CharField(max_length=50,unique=True)
    bus_type = models.CharField( max_length=10,choices=choices.BusType.choices, default='Standard')
    capacity=models.IntegerField()  

    def __str__(self):
        return self.bus_model
    
    
    
    

class Route(models.Model):
    start_point=models.CharField(max_length=50)
    end_point=models.CharField(max_length=50)
    distance=models.IntegerField()
    estimated_time=models.DurationField() 

    def __str__(self):
        return f"{self.start_point}-{self.end_point}"
    
class Schedule(models.Model):
    bus=models.ForeignKey(Bus,on_delete=models.CASCADE)
    route=models.ForeignKey(Route,on_delete=models.CASCADE)
    Ticket_price = models.IntegerField()
    departure_time=models.TimeField()
    arrival_time=models.TimeField()
    date=models.DateField()

    def __str__(self):
        return f"{self.id}"
        # return f"{self.route.start_point}-{self.route.end_point}"
    
    class Meta:
        unique_together = ('bus', 'date', 'departure_time')
    

class Ticket(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    status = models.CharField(max_length=2, choices=choices.TicketStatus.choices, default='P')
    booking_date = models.DateField()

    class Meta:
        unique_together = ('schedule', 'seat_number')
        
    def clean(self):
        if self.seat_number <= 0:
            raise ValidationError("Seat number must be greater than 0.")

        bus_capacity = self.schedule.bus.capacity
        if self.seat_number > bus_capacity:
                raise ValidationError(
                f"Seat number cannot be greater than bus capacity ({bus_capacity})."
            )

    def save(self, *args, **kwargs):
        # clean() ko call karo save k pehle
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.seat_number}-{self.status}"
    

