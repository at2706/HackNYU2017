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
                       'patient': forms.PatientForm})

    def post(self, request):
        with transaction.atomic():
            userForm = forms.RegistrationForm(request.POST)
            patientForm = forms.PatientForm(request.POST)

            if userForm.is_valid() and patientForm.is_valid():
                user = userForm.save()
                patientForm.save(user=user)
                messages.success(request, 'User successfully registered.')
                return HttpResponseRedirect("/")
        return HttpResponseRedirect(reverse('hacknyu:register'))
