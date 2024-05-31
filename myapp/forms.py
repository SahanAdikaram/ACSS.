from django import forms
from .models import SymptomRecord

class SymptomForm(forms.ModelForm):
    class Meta:
        model = SymptomRecord
        fields = ['description', 'severity', 'symptom_type', 'multiple_choice', 'photo', 'voice_record']
