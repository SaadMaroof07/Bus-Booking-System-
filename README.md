# Bus Booking System Backend

The Bus Booking System Backend is a REST API for a bus ticket-booking application. It manages customer accounts, buses, routes, travel schedules, seat availability, and ticket bookings.

## Functionality

- Customers can search schedules by route and travel date, check available seats, and book tickets.
- Managers and superusers can manage buses, routes, and schedules.
- The system validates seat numbers against bus capacity and prevents the same seat from being booked twice for one schedule.
- Token authentication protects account and booking features, with role-based access for management operations.
- Ticket booking can send confirmation email through a configured email service.

## Technology

- Python 3.10+
- Django 5.2.5
- Django REST Framework and Token Authentication
- django-filter for schedule search
- SQLite for local development and PostgreSQL support through 
