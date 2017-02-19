import csv
import random
from django.db import transaction
from .models import Hospital, HospitalAddress, Insurance, Doctor


def add():
    count = 0
    f = open('Hospital_General_Information.csv')
    csvfile = csv.reader(f)
    next(csvfile, None)
    for row in csvfile:
        with transaction.atomic():
            try:
                hospital = Hospital.objects.create(
                    name=str(row[1]).title(), phone_number=int(row[7]))
                HospitalAddress.objects.create(hospital=hospital, address1=str(
                    row[2]).title(), city=str(row[3]).title(), state=str(row[4]), zipcode=int(row[5]))
            except Exception:
                count += 1
    print("Missed Entries" + count)


def add2():
    f = open('us_companies.csv')
    csvfile = csv.reader(f)
    next(csvfile, None)

    with transaction.atomic():
        for row in csvfile:
            types = row[17].split(',')
            if 'Health/Healthcare' in types:
                Insurance.objects.create(name=row[1])


def add3():
    f = open('doctors.txt')
    specialties = ['Gynecology', 'Pediatric Cardiology',
                   'Cardiothoracic Radiology', 'Dermatology', 'Orthopaedic Surgery',
                   'Neurotology', 'Rehabilitation', 'Cancer', 'Dentistry']
    hospitals = Hospital.objects.all()
    with transaction.atomic():
        for line in f:
            Doctor.objects.create(full_name=line,
                                  specialty=random.choice(specialties),
                                  hospital=random.choice(hospitals))
