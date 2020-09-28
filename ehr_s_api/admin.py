from django.contrib import admin
from .models import Patient, PatientDisease, Drug, Prescription, Disease, Measurement

# Register your models here.

admin.site.register(Patient)
admin.site.register(Disease)
admin.site.register(Prescription)
admin.site.register(Drug)
admin.site.register(PatientDisease)
admin.site.register(Measurement)
