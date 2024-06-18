from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)

class MoodRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mood_rating = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    unusual_behavior = models.CharField(max_length=3, default='No')

    def __str__(self):
        return f"{self.user.username} - {self.mood_rating} - {self.timestamp}"


class SymptomRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    symptom_type = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    severity = models.IntegerField(null=True, blank=True)
    mcq_answers = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.symptom_type} at {self.timestamp}"

class DoctorPatientRelationship(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='doctor_patients')
    patient = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='assigned_doctor')

    def __str__(self):
        return f"Doctor {self.doctor.username} - Patient {self.patient.username}"

    @classmethod
    def get_or_create_relationship(cls, doctor, patient):
        relationship, created = cls.objects.get_or_create(doctor=doctor, patient=patient)
        return relationship


class Feedback(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patient_feedback')
    feedback = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username} at {self.timestamp}"

class DoctorFeedback(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='doctor_feedbacks')
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='doctor_feedbacks_received')
    feedback = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.doctor.username} to {self.patient.username} at {self.timestamp}"
