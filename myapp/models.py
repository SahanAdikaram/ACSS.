# myapp/models.py
from django.db import models

class MoodRecord(models.Model):
    mood_rating = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mood_rating} at {self.timestamp}"

class SymptomRecord(models.Model):
    symptom_type = models.CharField(max_length=255)
    description = models.TextField()
    severity = models.IntegerField()
    multiple_choice = models.CharField(max_length=255, blank=True, null=True)
    voice_record = models.FileField(upload_to='voice_records/', blank=True, null=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

  