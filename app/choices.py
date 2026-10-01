from django.db import models

class UserRole(models.TextChoices):
    SUPERADMIN='SA','Super Admin'
    MANAGER='M','Manager'
    CUSTOMER='C','Customer'

class TicketStatus(models.TextChoices):
    BOOKED = 'B', 'Booked'
    CANCELLED = 'C', 'Cancelled'
    PENDING = 'P', 'Pending'
    COMPLETED = 'CM', 'Completed' 

class BusType(models.TextChoices):
    LUXURY = 'LUX', 'Luxury'
    SEMI_LUXURY = 'SLX', 'Semi Luxury'
    STANDARD = 'STD', 'Standard'       