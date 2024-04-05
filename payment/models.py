from email.policy import default
from ssl import Purpose
from django.db import models

from mixins import UUIDMixin


class Transactions(UUIDMixin):

    from_user = models.UUIDField(null=False, blank=False)
    to_doctor = models.UUIDField(null=False, blank=False)
    contact = models.CharField(max_length=50, blank=True, null=True)
    amount = models.FloatField(null=True, blank=True)
    currency = models.CharField(max_length=50, blank=True, null=True)
    payment_status = models.CharField(max_length=50, blank=True, null=True)
    payment_method = models.CharField(max_length=100, blank=True, null=True)
    gateway = models.CharField(max_length=50, blank=True, null=True)
    payment_data = models.JSONField(default=dict)
    payment_id = models.CharField(max_length=100,blank=True)
    order_id = models.CharField(max_length=100,default='')
    signature = models.CharField(max_length=100,default='')
    email = models.EmailField(blank=True, null=True)
    payment_created_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "Transaction %s" % self.uuid
    

class Seminar(UUIDMixin):

    from_user = models.UUIDField(null=False, blank=False)
    to_seminar = models.UUIDField(null=False, blank=False)
    contact = models.CharField(max_length=50, blank=True, null=True)
    amount = models.FloatField(null=True, blank=True)
    currency = models.CharField(max_length=50, blank=True, null=True)
    payment_status = models.CharField(max_length=50, blank=True, null=True)
    payment_method = models.CharField(max_length=100, blank=True, null=True)
    gateway = models.CharField(max_length=50, blank=True, null=True)
    payment_data = models.JSONField(default=dict)
    payment_id = models.CharField(max_length=100, unique=True)
    email = models.EmailField(blank=True, null=True)
    payment_created_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "Seminar %s" % self.uuid