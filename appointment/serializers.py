from rest_framework import serializers

from .models import Appointments, UserNotification, DoctorNotification
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields = "__all__"


class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotification
        fields = "__all__"

class DoctorNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorNotification
        fields = "__all__"