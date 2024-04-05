from django.db.models.signals import pre_save
from django.dispatch import receiver,Signal
from appointment.models import Appointments
from datetime import date
# # creating a signal
# isActive = Signal(providing_args=[])

# # receiver function
@receiver(pre_save,sender=Appointments)
def is_active_true(sender,**kwargs):
    print('is active signal working')
    
    today = date.today()
    appointments = Appointments.objects.all()
    for appointment in appointments:
        appointment_date = appointment.appointment_date.date()
        if appointment_date < today :
            appointment.is_active = 'False'
            appointment.save()



# @receiver(pre_save, sender = Appointments)
# def is_active_true(sender, instance, **kwargs):
#    pass