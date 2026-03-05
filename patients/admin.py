from django.contrib import admin
from .models import (
    Patient, MedicalRecord, Medication,
    Prescription, Appointment,
)


class MedicalRecordInline(admin.TabularInline):
    model = MedicalRecord
    extra = 0


class AppointmentInline(admin.TabularInline):
    model = Appointment
    extra = 0


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = [
        'last_name', 'first_name', 'date_of_birth',
        'gender', 'blood_type', 'phone',
    ]
    list_filter = ['gender', 'blood_type']
    search_fields = ['first_name', 'last_name', 'phone', 'email']
    inlines = [MedicalRecordInline, AppointmentInline]


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'diagnosis', 'doctor', 'date']
    list_filter = ['date']
    search_fields = ['diagnosis', 'patient__first_name', 'patient__last_name']


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'dosage_form', 'manufacturer']
    list_filter = ['dosage_form']
    search_fields = ['name', 'manufacturer']


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'dosage', 'frequency', 'start_date']
    list_filter = ['start_date']
    filter_horizontal = ['medications']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'date_time', 'status', 'reason']
    list_filter = ['status', 'date_time']
    search_fields = [
        'patient__first_name', 'patient__last_name', 'reason',
    ]
