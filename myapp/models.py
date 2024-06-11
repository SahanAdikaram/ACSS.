from django.contrib.auth.models import User
from django.db import models

class MoodRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default= 2)
    mood_rating = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mood_rating} at {self.timestamp}"

class SymptomRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default= 2)
    symptom_type = models.CharField(max_length=255)
    description = models.TextField()
    severity = models.IntegerField()
    mcq_answers = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symptom_type} at {self.timestamp}"
