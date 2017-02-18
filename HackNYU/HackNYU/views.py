from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from . import forms

# Create your views here.


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html',
                      {'register': forms.RegistrationForm,
                       'patient': forms.PatientForm,
                       'doctor': forms.DoctorForm})

    def post(self, request):
        userForm = forms.RegistrationForm(request.POST)
        patientForm = forms.PatientForm(request.POST)
        doctorForm = forms.DoctorForm(request.POST)

        with transaction.atomic():
            if userForm.is_valid():
                user = userForm.save()
                if patientForm.is_valid():
                    patientForm.save(user=user)
                    messages.success(request, 'Patient successfully registered.')
                elif doctorForm.is_valid():
                    doctorForm.save(user=user)
                    messages.success(request, 'Doctor successfully registered.')
                return HttpResponseRedirect("/")

        return render(request, 'register.html',
                      {'register': userForm,
                       'patient': patientForm,
                       'doctor': doctorForm})
