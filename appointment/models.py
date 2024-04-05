from hashlib import blake2s
from django.db import models
from mixins import UUIDMixin
from django.utils import timezone
from usermgmt.models import User

STATUS = (('confirmed', 'Confirmed'), ('not_confirmed', 'Not_Confirmed'))
class Appointments(UUIDMixin):
    user_profile = models.UUIDField(null=False, blank=False)
    doctor = models.UUIDField(null=False, default=False)
    appointment_date = models.DateTimeField(default=timezone.now)
    appointment_time = models.TimeField(blank=True)
    fees = models.DecimalField(max_digits=7, decimal_places=2)
    booking_status = models.CharField(max_length=20, choices=STATUS, default='not_confirmed')
    transaction = models.UUIDField(null=False)
    booking_date = models.DateField(default=timezone.now)
    prescription = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

class UserNotification(UUIDMixin):
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        db_index=True,
        related_name="user_profile_info"
    )
    message = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)

class DoctorNotification(UUIDMixin):
    doctor = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        db_index=True,
        related_name="doctor_profile_info"
    )
    message = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)
    acceptance = models.CharField(max_length=20, choices=STATUS, default="not_confirmed")
