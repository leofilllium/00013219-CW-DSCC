from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from patients.models import (
    Patient, MedicalRecord, Medication,
    Prescription,
)
from datetime import date


class UserRegistrationTest(TestCase):
    """Test user registration functionality."""

    def test_register_creates_user(self):
        """Registration with valid data creates a new user."""
        response = self.client.post(reverse('register'), {
            'username': 'testdoc',
            'email': 'doc@example.com',
            'first_name': 'Test',
            'last_name': 'Doctor',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testdoc').exists())

    def test_login_redirects_to_dashboard(self):
        """Successful login redirects to the dashboard."""
        User.objects.create_user(
            username='testdoc', password='pass1234'
        )
        response = self.client.post(reverse('login'), {
            'username': 'testdoc',
            'password': 'pass1234',
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/dashboard/', response.url)


class PatientModelTest(TestCase):
    """Test Patient model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='doc', password='pass1234'
        )
        self.patient = Patient.objects.create(
            first_name='Jane',
            last_name='Doe',
            date_of_birth=date(1990, 5, 15),
            gender='F',
            blood_type='A+',
            created_by=self.user,
        )

    def test_patient_str(self):
        """Patient __str__ returns 'Last, First'."""
        self.assertEqual(str(self.patient), 'Doe, Jane')

    def test_patient_full_name(self):
        """Patient full_name property returns 'First Last'."""
        self.assertEqual(self.patient.full_name, 'Jane Doe')


class MedicalRecordTest(TestCase):
    """Test MedicalRecord creation with FK."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='doc', password='pass1234'
        )
        self.patient = Patient.objects.create(
            first_name='John',
            last_name='Smith',
            date_of_birth=date(1985, 3, 10),
            gender='M',
            created_by=self.user,
        )

    def test_record_creation(self):
        """Creating a medical record links to patient."""
        record = MedicalRecord.objects.create(
            patient=self.patient,
            doctor=self.user,
            diagnosis='Common Cold',
            symptoms='Cough, fever',
        )
        self.assertEqual(record.patient, self.patient)
        self.assertEqual(self.patient.medical_records.count(), 1)


class PrescriptionManyToManyTest(TestCase):
    """Test Prescription M2M relationship with Medications."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='doc', password='pass1234'
        )
        self.patient = Patient.objects.create(
            first_name='Alice', last_name='Wong',
            date_of_birth=date(1975, 8, 20), gender='F',
            created_by=self.user,
        )
        self.med1 = Medication.objects.create(
            name='Amoxicillin', dosage_form='capsule'
        )
        self.med2 = Medication.objects.create(
            name='Ibuprofen', dosage_form='tablet'
        )

    def test_prescription_m2m(self):
        """Prescription can have multiple medications."""
        rx = Prescription.objects.create(
            patient=self.patient, doctor=self.user,
            dosage='500mg', frequency='Every 8 hours',
            start_date=date.today(),
        )
        rx.medications.add(self.med1, self.med2)
        self.assertEqual(rx.medications.count(), 2)
        self.assertIn(self.med1, rx.medications.all())


class PatientViewsTest(TestCase):
    """Test patient list view requires auth."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='doc', password='pass1234'
        )

    def test_patient_list_unauthenticated(self):
        """Unauthenticated user is redirected to login."""
        response = self.client.get(reverse('patient-list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_patient_list_authenticated(self):
        """Authenticated user can access patient list."""
        self.client.login(username='doc', password='pass1234')
        response = self.client.get(reverse('patient-list'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_authenticated(self):
        """Authenticated user can access dashboard."""
        self.client.login(username='doc', password='pass1234')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
