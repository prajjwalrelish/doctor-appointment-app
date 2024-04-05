from mixins import UUIDMixin
from operator import mod
import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.contrib.postgres.fields import ArrayField
from django.db import models
from pytz import timezone


class LivLifeUserManager(UserManager):
    """Custom User Manager."""

    def create_first_superuser(self):
        """Check if admin users are present.

        If no admin users are present
        Then create an admin user

        Returns:
            The return value. Object for success, None otherwise.
        """
        if User.objects.filter(is_superuser=True).count() == 0:
            return super(LivLifeUserManager, self).create_superuser(
                email="admin@livlife.com", username="admin@livlife.com",
                password="livlife")
        return None


class User(AbstractUser):
    """ User model creation"""

    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    GENDER = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    )
    default = uuid.uuid4
    uuid = models.UUIDField(
        default=default,
        editable=False,
        help_text="A unique number to identify the user",
        primary_key=True
    )   
    id = models.UUIDField(default=default)
    gender = models.CharField(max_length=10, choices=GENDER, null=True, blank=True)
    mobile_number = models.CharField(max_length=12, null=True, blank=True)
    address = models.TextField(max_length=500, null=True)
    photo_url = models.URLField(default='https://unsplash.com/photos/s5kTY-Ve1c0', null=True, help_text="An optional image of the user")
    preferred_languages = ArrayField(
        models.CharField(max_length=5),
        default=None,
        null=True,
        help_text="Language codes of preferred languages in the order of preference"
    )
    timezones = ArrayField(
        models.CharField(max_length=20),
        default=None,
        null=True
    )
    DOB = models.DateField(null=True)
    about = models.TextField(null=True)
    is_Doctor = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    objects = LivLifeUserManager()  
    
    def __str__(self):
        return f'{ self.username} {self.uuid} '

# class UserProfile(models.Model):
#     """Extends the User Details"""
#     user = models.OneToOneField(
#         User,
#         on_delete=models.PROTECT,
#         related_name="profile",
#         db_index=True,
#     )
#     date_of_birth = models.DateField(null=True)
#     description = models.TextField(null=True)


class DoctorProfile(UUIDMixin):
    """ Extends Doctor Profile """
    # doctor_id = models.UUIDField(default=uuid.uuid4)
    doctor = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    designation = models.CharField(max_length=40, null=True, blank=True, default="")
    fees = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)
    working_hours = ArrayField(
        models.CharField(max_length=20),
        default=None,
        null=True
    )
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f'{ self.doctor.username} {self.uuid} '