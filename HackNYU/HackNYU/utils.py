import csv
from django.db import transaction
from .models import Hospital, HospitalAddress, Insurance


def add():
    f = open('Hospital_General_Information.csv')
    csvfile = csv.reader(f)
    next(csvfile, None)
    with transaction.atomic():
        for row in csvfile:
            hospital = Hospital.objects.create(name=str(row[1]).title(), phone_number=int(row[7]))
            HospitalAddress.objects.create(hospital=hospital, address1=str(
                row[2]).title(), city=str(row[3]).title(), state=str(row[4]), zipcode=int(row[5]))


def add2():
    f = open('us_companies.csv')
    csvfile = csv.reader(f)
    next(csvfile, None)

    with transaction.atomic():
        for row in csvfile:
            types = row[17].split(',')
            if 'Health/Healthcare' in types:
                Insurance.objects.create(name=row[1])
