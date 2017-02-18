from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

import csv
import os

# Create your models here.


class Patient(models.Model):
    user = models.OneToOneField(User, related_name='patient', on_delete=models.CASCADE)
    date_of_birth = models.DateField(default=None, blank=True, null=True)
    gender_choices = (('m', 'Male'), ('f', 'Female'), ('o', 'Other'))
    gender = models.CharField(max_length=1, choices=gender_choices, default='m')


class Doctor(models.Model):
    user = models.OneToOneField(User, related_name='doctor', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Name', max_length=50)
    department = models.CharField(verbose_name='Department', max_length=50)


class Address(models.Model):
    address1 = models.CharField(verbose_name='Address Line 1', max_length=30)
    address2 = models.CharField(verbose_name='Address Line 2', max_length=30, blank=True)
    city = models.CharField(verbose_name='City', max_length=10)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, 'states.csv')) as f:
        csvfile = csv.reader(f)
        state_choices = [(row[0], row[1]) for row in csvfile]
    state = models.CharField(verbose_name='State', max_length=2, choices=state_choices)

    class Meta:
        abstract = True


class UserAddress(Address):
    user = models.OneToOneField(User, related_name='address', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'user addresses'


class Hospital(models.Model):
    name = models.CharField(verbose_name='Name', max_length=50)


class HospitalAddress(Address):
    hospital = models.ForeignKey(Hospital, related_name='addresses', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'hospital addresses'


class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, related_name='records', null=True, on_delete=models.SET_NULL)
    doctor = models.ForeignKey(Doctor, related_name='records', null=True, on_delete=models.SET_NULL)
    date = models.DateField(auto_now_add=True)
    test_type = models.CharField(verbose_name='Test Type', max_length=50)
