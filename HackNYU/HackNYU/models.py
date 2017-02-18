from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Patient(models.Model):
    user = models.OneToOneField(User, related_name='details', on_delete=models.CASCADE)
    date_of_birth = models.DateField(default=None, blank=True, null=True)
    gender_choices = (('m', 'Male'), ('f', 'Female'), ('o', 'Other'))
    gender = models.CharField(max_length=1, choices=gender_choices, default='m')
