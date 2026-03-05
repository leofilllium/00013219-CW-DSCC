from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Patient(models.Model):
    """Patient profile storing personal and contact information."""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_type = models.CharField(
        max_length=3, choices=BLOOD_TYPE_CHOICES, blank=True
    )
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='patients_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    def get_absolute_url(self):
        return reverse('patient-detail', kwargs={'pk': self.pk})

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class MedicalRecord(models.Model):
    """Medical record linked to a patient (Many-to-One)."""
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE,
        related_name='medical_records'
    )
    doctor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='medical_records'
    )
    diagnosis = models.CharField(max_length=255)
    symptoms = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.diagnosis} – {self.patient}'


class Medication(models.Model):
    """Medication catalogue."""
    DOSAGE_FORM_CHOICES = [
        ('tablet', 'Tablet'),
        ('capsule', 'Capsule'),
        ('syrup', 'Syrup'),
        ('injection', 'Injection'),
        ('cream', 'Cream'),
        ('drops', 'Drops'),
        ('inhaler', 'Inhaler'),
    ]

    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    dosage_form = models.CharField(
        max_length=20, choices=DOSAGE_FORM_CHOICES, default='tablet'
    )
    manufacturer = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.get_dosage_form_display()})'


class Prescription(models.Model):
    """Prescription linking patients and medications (Many-to-Many)."""
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE,
        related_name='prescriptions'
    )
    doctor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='prescriptions_written'
    )
    medications = models.ManyToManyField(
        Medication, related_name='prescriptions'
    )
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(
        max_length=100,
        help_text='e.g. Twice daily, Every 8 hours'
    )
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        meds = ', '.join(m.name for m in self.medications.all()[:3])
        return f'Rx: {meds} – {self.patient}'


class Appointment(models.Model):
    """Appointment scheduling for patients (Many-to-One)."""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE,
        related_name='appointments'
    )
    doctor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='appointments'
    )
    date_time = models.DateTimeField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='scheduled'
    )
    reason = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_time']

    def __str__(self):
        return f'{self.patient} – {self.date_time:%Y-%m-%d %H:%M}'
