from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.detail import DetailView

from geopy.distance import vincenty
import operator

from . import forms
from . import models
# Create your views here.


class IndexView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        recent = models.LabReport.objects.filter(
            patient=request.user.patient).order_by("-date")[:5]
        return render(request, 'index.html', {'recent': recent})

    def post(self, request):
        if request.is_ajax():
            print("Hello!")
            lat = request.POST.get('lat')
            lng = request.POST.get('lng')
            pos = (lat, lng)

            nearby = []
            for hospital in models.HospitalAddress.objects.all():
                loc = (hospital.lat, hospital.lng)
                nearby.append((hospital, vincenty(pos, loc).miles))

            nearby.sort(key=operator.itemgetter(1))
            return JsonResponse(nearby[:10])

        return HttpResponse()


class LabReportDetail(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'next'
    model = models.LabReport
    template_name = "detail.html"

    def get(self, request, pk):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/login")
        return super(LabReportDetail, self).get(request, pk)


class HistoryView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        all_reports = models.LabReport.objects.filter(
            patient=request.user.patient).order_by("-date")
        return render(request, 'history.html',
                      {'reports': all_reports})


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html',
                      {'register': forms.RegistrationForm,
                       'patient': forms.PatientForm,
                       'address': forms.UserAddressForm})

    def post(self, request):
        userForm = forms.RegistrationForm(request.POST)
        patientForm = forms.PatientForm(request.POST)
        addressForm = forms.UserAddressForm(request.POST)

        with transaction.atomic():
            if userForm.is_valid() and patientForm.is_valid() and addressForm.is_valid():
                user = userForm.save()
                patientForm.save(user=user)
                addressForm.save(user=user)
                messages.success(request, 'Patient successfully registered.')
                return HttpResponseRedirect("/")

        return render(request, 'register.html',
                      {'register': userForm,
                       'patient': patientForm, 
                       'address': addressForm})


class DoctorView(View):
    def get(self, request):
        return render(request, 'doctor.html')


class FaqView(View):
    def get(self, request):
        return render(request, 'faq.html')


class HelpView(View):
    def get(self, request):
        return render(request, 'help.html')


class SecurityView(View):
    def get(self, request):
        return render(request, 'security.html')


class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')


class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html')
