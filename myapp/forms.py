from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import SymptomRecord

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class HallucinationsForm(forms.ModelForm):
    hallucinations_q1 = forms.ChoiceField(choices=[('A', 'Frequently'), ('B', 'Occasionally'), ('C', 'Rarely'), ('D', 'Never')], label="Question 1: In the past week, has the patient reported hearing voices that others do not hear?")
    hallucinations_q2 = forms.ChoiceField(choices=[('A', 'Yes, frequently'), ('B', 'Yes, a few times'), ('C', 'Yes, once'), ('D', 'No, never')], label="Question 2: Has the patient seen things that others cannot see within the last month?")
    hallucinations_q3 = forms.ChoiceField(choices=[('A', 'Yes, always'), ('B', 'Yes, sometimes'), ('C', 'Yes, but rarely'), ('D', 'No, never')], label="Question 3: Does the patient believe they have special powers or abilities that others do not possess?")
    hallucinations_q4 = forms.ChoiceField(choices=[('A', 'Often'), ('B', 'Occasionally'), ('C', 'Seldom'), ('D', 'Never')], label="Question 4: Has the patient expressed fear that others are plotting against them or trying to harm them?")
    
    class Meta:
        model = SymptomRecord
        fields = ['description', 'severity']
        widgets = {
            'mcq_answers': forms.HiddenInput()  # Store the JSON data in a hidden field
        }

class FlatteningForm(forms.ModelForm):
    flattening_q1 = forms.ChoiceField(choices=[('A', 'Very often'), ('B', 'Sometimes'), ('C', 'Rarely'), ('D', 'Never')], label="Question 1: How often does the patient display a lack of emotional expression (e.g., not smiling, lack of facial expressions)?")
    flattening_q2 = forms.ChoiceField(choices=[('A', 'Frequently'), ('B', 'Occasionally'), ('C', 'Rarely'), ('D', 'Never')], label="Question 2: Has the patient shown a reduced ability to express emotions (e.g., through gestures, tone of voice) recently?")
    flattening_q3 = forms.ChoiceField(choices=[('A', 'Very frequently'), ('B', 'Often'), ('C', 'Sometimes'), ('D', 'Never')], label="Question 3: Has the patient been speaking less frequently or with fewer words than usual?")
    flattening_q4 = forms.ChoiceField(choices=[('A', 'Yes, very often'), ('B', 'Yes, sometimes'), ('C', 'Yes, but rarely'), ('D', 'No, never')], label="Question 4: Does the patient often have difficulty finding the right words to express themselves?")
    
    class Meta:
        model = SymptomRecord
        fields = ['description', 'severity']
        widgets = {
            'mcq_answers': forms.HiddenInput()
        }

class AvolitionForm(forms.ModelForm):
    avolition_q1 = forms.ChoiceField(choices=[('A', 'Very often'), ('B', 'Often'), ('C', 'Sometimes'), ('D', 'Never')], label="Question 1: Has the patient shown a lack of motivation to start or complete tasks?")
    avolition_q2 = forms.ChoiceField(choices=[('A', 'Almost always'), ('B', 'Frequently'), ('C', 'Occasionally'), ('D', 'Never')], label="Question 2: How often does the patient seem uninterested in participating in daily activities?")
    
    class Meta:
        model = SymptomRecord
        fields = ['description', 'severity']
        widgets = {
            'mcq_answers': forms.HiddenInput()
        }

class DifficultyConcentratingForm(forms.ModelForm):
    difficulty_concentrating_q1 = forms.ChoiceField(choices=[('A', 'Very often'), ('B', 'Often'), ('C', 'Sometimes'), ('D', 'Never')], label="Question 1: Has the patient had trouble concentrating on tasks or conversations recently?")
    difficulty_concentrating_q2 = forms.ChoiceField(choices=[('A', 'Always'), ('B', 'Often'), ('C', 'Sometimes'), ('D', 'Never')], label="Question 2: How frequently does the patient appear easily distracted?")
    difficulty_concentrating_q3 = forms.ChoiceField(choices=[('A', 'Very frequently'), ('B', 'Often'), ('C', 'Occasionally'), ('D', 'Never')], label="Question 3: Does the patient have difficulty remembering appointments or daily tasks?")
    difficulty_concentrating_q4 = forms.ChoiceField(choices=[('A', 'Very often'), ('B', 'Often'), ('C', 'Sometimes'), ('D', 'Never')], label="Question 4: How often does the patient forget recent conversations or events?")
    difficulty_concentrating_q5 = forms.ChoiceField(choices=[('A', 'Very frequently'), ('B', 'Often'), ('C', 'Sometimes'), ('D', 'Never')], label="Question 5: Has the patient shown indecisiveness or difficulty making decisions?")
    difficulty_concentrating_q6 = forms.ChoiceField(choices=[('A', 'Almost always'), ('B', 'Often'), ('C', 'Occasionally'), ('D', 'Never')], label="Question 6: How often does the patient take a long time to make simple decisions?")
    
    class Meta:
        model = SymptomRecord
        fields = ['description', 'severity']
        widgets = {
            'mcq_answers': forms.HiddenInput()
        }

class SocialCognitionForm(forms.ModelForm):
    social_cognition_q1 = forms.ChoiceField(choices=[('A', 'Very often'), ('B', 'Often'), ('C', 'Sometimes'), ('D', 'Never')], label="Question 1: Has the patient had trouble understanding social cues or body language?")
    social_cognition_q2 = forms.ChoiceField(choices=[('A', 'Very frequently'), ('B', 'Often'), ('C', 'Occasionally'), ('D', 'Never')], label="Question 2: How frequently does the patient struggle to engage in social interactions or maintain relationships?")
    
    class Meta:
        model = SymptomRecord
        fields = ['description', 'severity']
        widgets = {
            'mcq_answers': forms.HiddenInput()
        }
