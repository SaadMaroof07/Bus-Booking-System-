from rest_framework import serializers
from app import models

class CustomUser_Serializer(serializers.ModelSerializer):
    class Meta:
        model=models.CustomUser
        fields=['username', 'password','email', 'role', 'phone_number']
        read_only_fields = ['role']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8}
            }


    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password=validated_data.pop('password',None)
        for attr,value in validated_data.items():
            setattr(instance,attr,value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance   


class Bus_Serializer(serializers.ModelSerializer):
    class Meta:
        model=models.Bus
        fields=['id','bus_model','bus_number', 'bus_type', 'capacity']        


class Route_Serializer(serializers.ModelSerializer):
    class Meta:
        model=models.Route
        fields=['id','start_point', 'end_point', 'distance', 'estimated_time']


class Schedule_Serializer(serializers.ModelSerializer):
    bus_type = serializers.CharField(source='bus.bus_type', read_only=True)
    start_point=serializers.CharField(source='route.start_point',read_only=True)
    end_point=serializers.CharField(source='route.end_point',read_only=True)
    seats_available=serializers.SerializerMethodField()

    class Meta:
        model=models.Schedule
        fields=['id','bus', 'bus_type','start_point','end_point','route','Ticket_price', 'departure_time', 'arrival_time', 'date','seats_available']

    def get_seats_available(self, obj):
        # BUG FIX 3: Return sorted list instead of set for JSON serialization
        bus_capacity = obj.bus.capacity 
        all_seats = set(range(1, bus_capacity + 1))
        booked = set(models.Ticket.objects.filter(schedule=obj.id).values_list('seat_number', flat=True))
        avaiable_seats = all_seats - booked
        return sorted(list(avaiable_seats))  # Convert set to sorted list for JSON serialization





class Ticket_Serializer(serializers.ModelSerializer):
    class Meta:
        model=models.Ticket
        fields=['id','customer', 'schedule', 'seat_number', 'status', 'booking_date'] 
        extra_kwargs = {
            'customer': {'read_only': True}
        }      

              








