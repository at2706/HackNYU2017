from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic.detail import DetailView
from . import forms
from . import models

# Create your views here.


class IndexView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/login")
        recent = models.LabReport.objects.filter(patient=request.user.patient).order_by("-date")[:5]
        return render(request, 'index.html', {'recent': recent})

    def post(self, request):
        if request.is_ajax():
            print("Hello!")

        return HttpResponse()


class LabReportDetail(DetailView):
    model = models.LabReport
    template_name = "detail.html"

    def get(self, request, pk):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/login")
        return super(LabReportDetail, self).get(request, pk)


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html',
                      {'register': forms.RegistrationForm,
                       'patient': forms.PatientForm})

    def post(self, request):
        userForm = forms.RegistrationForm(request.POST)
        patientForm = forms.PatientForm(request.POST)

        with transaction.atomic():
            if userForm.is_valid():
                user = userForm.save()
                if patientForm.is_valid():
                    patientForm.save(user=user)
                    messages.success(request, 'Patient successfully registered.')
                return HttpResponseRedirect("/")

        return render(request, 'register.html',
                      {'register': userForm,
                       'patient': patientForm})


class HistoryView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/login")
        all_reports = models.LabReport.objects.filter(patient=request.user.patient).order_by("-date")
        return render(request, 'history.html',
                      {'reports': all_reports})
