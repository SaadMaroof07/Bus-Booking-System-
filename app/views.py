from django.shortcuts import render
from rest_framework import viewsets
from app import models
from app import serializers
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from app.permissions import IsSuperUser, IsManager_or_superuser
from django_filters.rest_framework import DjangoFilterBackend
from app import filters

# Create your views here.

class SignUpViewSet(viewsets.ModelViewSet):
    queryset=models.CustomUser.objects.all()
    serializer_class=serializers.CustomUser_Serializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsSuperUser()]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "User created successfully."},
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=['POST'], permission_classes=[IsSuperUser])
    def make_manager(self,request,pk=None):
        try:
            user=models.CustomUser.objects.get(pk=pk)
            user.role='M'
            user.save()
            return Response({'message':'user is now the manager'},status=status.HTTP_200_OK)
        except models.CustomUser.DoesNotExist:
            return Response({'message':'this user does not exist'},status=status.HTTP_400_BAD_REQUEST)
class Bus_ViewSet(viewsets.ModelViewSet):
    permission_classes=[IsManager_or_superuser]
    queryset=models.Bus.objects.all()
    serializer_class=serializers.Bus_Serializer


class Route_ViewSet(viewsets.ModelViewSet):
    permission_classes=[IsManager_or_superuser]
    queryset=models.Route.objects.all()
    serializer_class=serializers.Route_Serializer 


class Schedule_ViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=models.Schedule.objects.all()
    serializer_class=serializers.Schedule_Serializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ScheduleFilter  

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return[IsManager_or_superuser()]
        return[IsAuthenticated()]



class Ticket_ViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=models.Ticket.objects.all()
    serializer_class=serializers.Ticket_Serializer 

    def get_queryset(self):
        # BUG FIX 5: Filter tickets by current user unless manager/superuser (privacy fix)
        user = self.request.user
        if user.role in ['M', 'S'] or user.is_superuser:  # Manager or Superuser
            return models.Ticket.objects.all()
        return models.Ticket.objects.filter(customer=user)  # Only own tickets for customers

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [IsManager_or_superuser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        data=request.data.copy()  # Create a mutable copy of request data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        ticket = serializer.save(customer=request.user)

        user = ticket.customer  

        # Email setup (simple)
        subject = "Ticket Purchased"
        message = f"Dear {user.username},\n\nThank you for purchasing your ticket. Have a safe journey!"
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient = user.email

        try:
            send_mail(subject, message, email_from, [recipient])
        except:
            return Response(
                {"error": "Ticket purchased but email not sent."},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"message": "Ticket purchased successfully. Confirmation email sent."},
            status=status.HTTP_201_CREATED,
        )





