from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import (
    Patient, MedicalRecord, Medication,
    Prescription, Appointment,
)
from .forms import (
    PatientForm, MedicalRecordForm, MedicationForm,
    PrescriptionForm, AppointmentForm,
)


def home(request):
    """Landing page."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')


@login_required
def dashboard(request):
    """Dashboard with summary statistics."""
    today = timezone.now().date()
    context = {
        'total_patients': Patient.objects.count(),
        'total_records': MedicalRecord.objects.count(),
        'total_prescriptions': Prescription.objects.count(),
        'upcoming_appointments': Appointment.objects.filter(
            date_time__date__gte=today, status='scheduled'
        ).count(),
        'recent_patients': Patient.objects.order_by('-created_at')[:5],
        'recent_appointments': Appointment.objects.filter(
            date_time__date__gte=today, status='scheduled'
        ).select_related('patient', 'doctor')[:5],
    }
    return render(request, 'patients/dashboard.html', context)


# ── Patient CRUD ────────────────────────────────────────────

@login_required
def patient_list(request):
    """List all patients with optional search."""
    query = request.GET.get('q', '')
    patients = Patient.objects.select_related('created_by')
    if query:
        patients = patients.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(phone__icontains=query)
        )
    return render(request, 'patients/patient_list.html', {
        'patients': patients, 'query': query,
    })


@login_required
def patient_detail(request, pk):
    """Patient detail with records, prescriptions, appointments."""
    patient = get_object_or_404(Patient, pk=pk)
    context = {
        'patient': patient,
        'records': patient.medical_records.select_related('doctor'),
        'prescriptions': patient.prescriptions.prefetch_related(
            'medications'
        ).select_related('doctor'),
        'appointments': patient.appointments.select_related('doctor'),
    }
    return render(request, 'patients/patient_detail.html', context)


@login_required
def patient_create(request):
    """Create a new patient."""
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.created_by = request.user
            patient.save()
            messages.success(request, 'Patient created successfully.')
            return redirect('patient-detail', pk=patient.pk)
    else:
        form = PatientForm()
    return render(request, 'patients/patient_form.html', {
        'form': form, 'title': 'Add New Patient',
    })


@login_required
def patient_update(request, pk):
    """Update an existing patient."""
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient updated successfully.')
            return redirect('patient-detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/patient_form.html', {
        'form': form, 'title': f'Edit {patient.full_name}',
    })


@login_required
def patient_delete(request, pk):
    """Delete a patient."""
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        messages.success(request, 'Patient deleted successfully.')
        return redirect('patient-list')
    return render(request, 'patients/patient_confirm_delete.html', {
        'patient': patient,
    })


# ── Medical Records ─────────────────────────────────────────

@login_required
def record_create(request, patient_pk):
    """Add a medical record to a patient."""
    patient = get_object_or_404(Patient, pk=patient_pk)
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = patient
            record.doctor = request.user
            record.save()
            messages.success(request, 'Medical record added.')
            return redirect('patient-detail', pk=patient.pk)
    else:
        form = MedicalRecordForm()
    return render(request, 'patients/record_form.html', {
        'form': form, 'patient': patient,
    })


# ── Prescriptions ───────────────────────────────────────────

@login_required
def prescription_list(request):
    """List all prescriptions."""
    prescriptions = Prescription.objects.select_related(
        'patient', 'doctor'
    ).prefetch_related('medications')
    return render(request, 'patients/prescription_list.html', {
        'prescriptions': prescriptions,
    })


@login_required
def prescription_create(request):
    """Create a new prescription."""
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.doctor = request.user
            prescription.save()
            form.save_m2m()
            messages.success(request, 'Prescription created.')
            return redirect('prescription-list')
    else:
        form = PrescriptionForm()
    return render(request, 'patients/prescription_form.html', {
        'form': form, 'title': 'New Prescription',
    })


# ── Appointments ─────────────────────────────────────────────

@login_required
def appointment_list(request):
    """List all appointments."""
    appointments = Appointment.objects.select_related('patient', 'doctor')
    return render(request, 'patients/appointment_list.html', {
        'appointments': appointments,
    })


@login_required
def appointment_create(request):
    """Create a new appointment."""
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = request.user
            appointment.save()
            messages.success(request, 'Appointment scheduled.')
            return redirect('appointment-list')
    else:
        form = AppointmentForm()
    return render(request, 'patients/appointment_form.html', {
        'form': form, 'title': 'Schedule Appointment',
    })


# ── Medications ──────────────────────────────────────────────

@login_required
def medication_list(request):
    """List all medications."""
    medications = Medication.objects.all()
    return render(request, 'patients/medication_list.html', {
        'medications': medications,
    })


@login_required
def medication_create(request):
    """Add a new medication to the catalogue."""
    if request.method == 'POST':
        form = MedicationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medication added.')
            return redirect('medication-list')
    else:
        form = MedicationForm()
    return render(request, 'patients/medication_form.html', {
        'form': form, 'title': 'Add Medication',
    })
