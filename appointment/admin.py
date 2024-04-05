from django.contrib import admin
from .models import UserNotification,Appointments,DoctorNotification
admin.site.register(Appointments)
admin.site.register(UserNotification)
admin.site.register(DoctorNotification)
# Register your models here.
