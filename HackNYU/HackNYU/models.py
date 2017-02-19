from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

import csv
from datetime import date
import os
from geopy.geocoders import Nominatim
dir_path = os.path.dirname(os.path.realpath(__file__))
# Create your models here.


class Insurance(models.Model):
    name = models.CharField(verbose_name='Name', max_length=50)

    def __str__(self):
        return self.name


class Patient(models.Model):
    user = models.OneToOneField(User, related_name='patient', on_delete=models.CASCADE)
    date_of_birth = models.DateField(default=None, blank=True, null=True)
    gender_choices = (('m', 'Male'), ('f', 'Female'), ('o', 'Other'))
    gender = models.CharField(max_length=1, choices=gender_choices, default='m')
    weight = models.IntegerField()
    insurance = models.OneToOneField(
        Insurance, related_name='patient', null=True, on_delete=models.SET_NULL)
    phone_number = models.IntegerField()

    def __str__(self):
        return str(self.user)

    def age(self):
        return int(date.today() - self.date_of_birth) / 365


class Address(models.Model):
    address1 = models.CharField(verbose_name='Address Line 1', max_length=30)
    address2 = models.CharField(verbose_name='Address Line 2', max_length=30, blank=True)
    city = models.CharField(verbose_name='City', max_length=10)

    with open(os.path.join(dir_path, 'states.csv')) as f:
        csvfile = csv.reader(f)
        state_choices = [(row[0], row[1]) for row in csvfile]
    state = models.CharField(verbose_name='State', max_length=2, choices=state_choices)
    zipcode = models.IntegerField()

    lat = models.DecimalField(max_digits=22, decimal_places=16, default=0)
    lng = models.DecimalField(max_digits=22, decimal_places=16, default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return " ".join([self.address1, self.address2, self.city, self.state, str(self.zipcode)])

    def save(self, *args, **kwargs):
        geolocator = Nominatim()
        try:
            location = geolocator.geocode(str(self))
            self.lat = location.latitude
            self.lng = location.longitude
        except Exception:
            pass
        super(Address, self).save(*args, **kwargs)


class UserAddress(Address):
    user = models.OneToOneField(User, related_name='address', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'user addresses'


class Hospital(models.Model):
    name = models.CharField(verbose_name='Name', max_length=50)
    phone_number = models.IntegerField()
    insurance = models.OneToOneField(
        Insurance, related_name='hospital', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def formatted_number(self):
        return "(" + str(self.phone_number)[0:3] + ") - " + str(self.phone_number)[3:6] + " - " + str(self.phone_number)[6:10]


class HospitalAddress(Address):
    hospital = models.OneToOneField(Hospital, related_name='address', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'hospital addresses'


class Doctor(models.Model):
    # user = models.OneToOneField(User, related_name='doctor', on_delete=models.CASCADE)
    full_name = models.CharField(verbose_name='Name', max_length=50, default='John Doe')
    specialty = models.CharField(verbose_name='Department', max_length=50)
    hospital = models.ForeignKey(Hospital, related_name='doctor', on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name


class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, related_name='records',
                                null=True, on_delete=models.SET_NULL)
    doctor = models.ForeignKey(Doctor, related_name='records',
                               null=True, on_delete=models.SET_NULL)
    date = models.DateField(auto_now_add=True)
    test_type = models.CharField(verbose_name='Test Type', max_length=50)

    def __str__(self):
        return str(self.patient.user) + " " + str(self.date)


class LabReport(models.Model):
    patient = models.ForeignKey(Patient, related_name='lab', null=True, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    illness = models.CharField(verbose_name='Illness', max_length=500)
    treatment = models.CharField(verbose_name='Treatment', max_length=500)
    weight = models.IntegerField()
    amount = models.IntegerField()
    category = models.CharField(verbose_name='Category', max_length=30)
    doctor = models.ForeignKey(Doctor, related_name='lab', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.patient.user) + " " + str(self.date)


class inpatient(models.Model):
    patient = models.ForeignKey(Patient, related_name='inpatient',
                                null=True, on_delete=models.SET_NULL)
    lab = models.ForeignKey(LabReport, related_name='inpatient',
                            null=True, on_delete=models.SET_NULL)
    date_of_admission = models.DateField(auto_now_add=True)
    date_of_discharge = models.DateField(auto_now_add=True)


class outpatient(models.Model):
    patient = models.ForeignKey(Patient, related_name='outpatient',
                                null=True, on_delete=models.SET_NULL)
    lab = models.ForeignKey(LabReport, related_name='outpatient',
                            null=True, on_delete=models.SET_NULL)
    date = models.DateField(auto_now_add=True)


class Room(models.Model):
    status = models.BooleanField(default=False)
    roomtype = models.CharField(verbose_name='Room', max_length=30)
