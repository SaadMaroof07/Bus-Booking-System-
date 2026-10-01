from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from app import models

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
   
    list_display = ('id','username', 'email', 'role', 'phone_number', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')

   
    search_fields = ('username', 'email', 'phone_number')

   
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Information', {
            'fields': ('role', 'phone_number'),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Information', {
            'fields': ('role', 'phone_number'),
        }),
    )


@admin.register(models.Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('bus_model','bus_number', 'bus_type', 'capacity')
    search_fields = ('bus_number', 'bus_type')


@admin.register(models.Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('start_point', 'end_point', 'distance', 'estimated_time')
    search_fields = ('start_point', 'end_point')    



@admin.register(models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id','bus', 'route','Ticket_price', 'departure_time', 'arrival_time', 'date')
    list_filter = ('date', 'bus', 'route')
    search_fields = ('bus__bus_number', 'route__start_point', 'route__end_point')



@admin.register(models.Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('customer', 'schedule', 'seat_number', 'status', 'booking_date')
    list_filter = ('status', 'booking_date')
    search_fields = ('customer__username', 'schedule__bus__bus_number', 'seat_number')