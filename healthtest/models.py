from datetime import datetime
from django.db import models
from mixins import UUIDMixin
from usermgmt.models import User
from django.contrib.postgres.fields import ArrayField
# Create your models here.
class Questions(UUIDMixin):
    
    question = models.TextField(null=False, blank=False)
    option1 = models.JSONField(null=True, blank=False)
    option2 =  models.JSONField(null=True, blank=False)
    option3 =  models.JSONField(null=True, blank=False)
    option4 =  models.JSONField(null=True, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    question_type = models.CharField(max_length=100 ,default="", null=True, blank=True)
    priority = models.IntegerField(default = 0)

    def __str__(self):
        return f'{ self.question} {self.uuid} '

class QuestionList(UUIDMixin):

    questions = ArrayField(
        models.UUIDField(blank=True),
        default=None,
        null=True
    )
    no_of_question = models.BigIntegerField(default=0, null=True)
    test_type = models.CharField(max_length=100, default= "", null=True, blank=True)
    disease_type = models.CharField(max_length=100, null=True, blank=True)
    created_date  = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


class UserMentalHealth(UUIDMixin):

    user = models.OneToOneField(
        User,
        related_name= "mental_health_status",
        on_delete=models.CASCADE
    )
    score = models.BigIntegerField(default=0, blank=True)
    doctors = ArrayField(
        models.UUIDField(blank=True),
        default=None,
        null=True
    )
    tests = models.JSONField(null=True)
    created_date  = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_taken = models.BooleanField(default=False)

