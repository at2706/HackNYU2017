from django.shortcuts import render
from django.views import View

from . import forms

# Create your views here.


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html', {'register': forms.RegistrationForm})
