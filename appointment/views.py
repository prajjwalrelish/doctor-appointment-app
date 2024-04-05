from django.http import request
from django.shortcuts import render
from .models import Appointments,UserNotification,DoctorNotification
from rest_framework.permissions import IsAuthenticated
from .serializers import AppointmentSerializer,UserNotificationSerializer,DoctorNotificationSerializer
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from . import signals
# Create your views here.
class AppointmentViewSet(viewsets.ModelViewSet):
    # signals.isActive.send(sender=None)
    queryset = Appointments.objects.all()
    serializer_class = AppointmentSerializer
    filterset_fields = ['is_active']
    
    def get_queryset(self):
        user = self.request.user
        return Appointments.objects.filter(user_profile=user.id)
    
class UserNotificationViewSet(viewsets.ModelViewSet):
    queryset = UserNotification.objects.all()
    serializer_class = UserNotificationSerializer
    filterset_fields = ['is_active']

    # def get_queryset(self):
    #     user = self.request.user
    #     return UserNotification.objects.filter(user=user)
    
class DoctorNotificationViewSet(viewsets.ModelViewSet):
    queryset = DoctorNotification.objects.all()
    serializer_class = DoctorNotificationSerializer
    filterset_fields = ['is_active']

    # def get_queryset(self):
    #     doctor = self.request.user
    #     return DoctorNotification.objects.filter(doctor=doctor)