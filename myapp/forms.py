from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import SymptomRecord, CustomUser, DoctorPatientRelationship, DoctorFeedback

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']

class LoginForm(AuthenticationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'role']

class HallucinationsForm(forms.ModelForm):
    hearing_voices = forms.ChoiceField(choices=[('Yes', 'Yes'), ('No', 'No')], label="Hearing Voices")
    seeing_unreal_objects = forms.ChoiceField(choices=[('Yes', 'Yes'), ('No', 'No')], label="Seeing Unreal Objects")
    severity = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = SymptomRecord
        fields = ['hearing_voices', 'seeing_unreal_objects', 'severity']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class DelusionsForm(forms.ModelForm):
    special_powers = forms.ChoiceField(choices=[('Yes', 'Yes'), ('No', 'No')], label="Special Powers")
    fear_of_plots = forms.ChoiceField(choices=[('Yes', 'Yes'), ('No', 'No')], label="Fear of Plots")
    severity = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = SymptomRecord
        fields = ['special_powers', 'fear_of_plots', 'severity']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class FlatteningForm(forms.ModelForm):
    lack_of_emotion = forms.ChoiceField(choices=[('Yes', 'Yes'), ('No', 'No')], label="Lack of Emotion")
    reduced_speech = forms.ChoiceField(choices=[('Yes', 'Yes'), ('No', 'No')], label="Reduced Speech")
    severity = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = SymptomRecord
        fields = ['lack_of_emotion', 'reduced_speech', 'severity']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class AvolitionForm(forms.ModelForm):
    lack_of_motivation = forms.ChoiceField(choices=[('Yes', 'Yes'), ('No', 'No')], label="Lack of Motivation")
    disinterest_in_activities = forms.ChoiceField(choices=[('Yes', 'Yes'), ('No', 'No')], label="Disinterest in Activities")
    severity = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = SymptomRecord
        fields = ['lack_of_motivation', 'disinterest_in_activities', 'severity']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ConcentrationMemoryForm(forms.ModelForm):
    trouble_concentrating = forms.ChoiceField(choices=[('Yes', 'Yes'), ('No', 'No')], label="Trouble Concentrating")
    forgetfulness = forms.ChoiceField(choices=[('Yes', 'Yes'), ('No', 'No')], label="Forgetfulness")
    severity = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = SymptomRecord
        fields = ['trouble_concentrating', 'forgetfulness', 'severity']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class SocialCognitionForm(forms.ModelForm):
    social_cues = forms.ChoiceField(choices=[('Yes', 'Yes'), ('No', 'No')], label="Social Cues")
    social_interaction_issues = forms.ChoiceField(choices=[('Yes', 'Yes'), ('No', 'No')], label="Social Interaction Issues")
    severity = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = SymptomRecord
        fields = ['social_cues', 'social_interaction_issues', 'severity']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class AssignDoctorForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=CustomUser.objects.filter(role='doctor'), required=True, label="Select Doctor")

    class Meta:
        model = DoctorPatientRelationship
        fields = ['doctor']

class DoctorFeedbackForm(forms.ModelForm):
    class Meta:
        model = DoctorFeedback
        fields = ['feedback']
        

class AddPatientForm(forms.Form):
    patient_username = forms.CharField(max_length=150, required=True, label="Patient Username")

    def clean_patient_username(self):
        username = self.cleaned_data.get('patient_username')
        try:
            patient = CustomUser.objects.get(username=username, role='patient')
        except CustomUser.DoesNotExist:
            raise forms.ValidationError("No patient found with this username.")
        return patient
