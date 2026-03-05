from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Patients
    path('patients/', views.patient_list, name='patient-list'),
    path('patients/add/', views.patient_create, name='patient-create'),
    path('patients/<int:pk>/', views.patient_detail, name='patient-detail'),
    path(
        'patients/<int:pk>/edit/', views.patient_update,
        name='patient-update',
    ),
    path(
        'patients/<int:pk>/delete/', views.patient_delete,
        name='patient-delete',
    ),

    # Medical records
    path(
        'patients/<int:patient_pk>/records/add/',
        views.record_create, name='record-create',
    ),

    # Prescriptions
    path(
        'prescriptions/', views.prescription_list,
        name='prescription-list',
    ),
    path(
        'prescriptions/add/', views.prescription_create,
        name='prescription-create',
    ),

    # Appointments
    path(
        'appointments/', views.appointment_list,
        name='appointment-list',
    ),
    path(
        'appointments/add/', views.appointment_create,
        name='appointment-create',
    ),

    # Medications
    path(
        'medications/', views.medication_list,
        name='medication-list',
    ),
    path(
        'medications/add/', views.medication_create,
        name='medication-create',
    ),
]
