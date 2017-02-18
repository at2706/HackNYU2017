from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Patient)
admin.site.register(models.Doctor)
admin.site.register(models.UserAddress)
admin.site.register(models.Doctor)
admin.site.register(models.Hospital)
admin.site.register(models.HospitalAddress)
admin.site.register(models.MedicalRecord)
admin.site.register(models.LabReport)
admin.site.register(models.inpatient)
admin.site.register(models.outpatient)
admin.site.register(models.Room)
