import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import MoodRecord, SymptomRecord
from .forms import (RegisterForm, HallucinationsForm, FlatteningForm, AvolitionForm, 
                    DifficultyConcentratingForm, SocialCognitionForm)

def landing(request):
    return render(request, 'landing.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('select_mood')  
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('select_mood') 
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('landing')
@login_required
def show_mood_selection(request):
    return render(request, 'select_mood.html')

@csrf_exempt
@login_required
def record_mood(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mood = data.get('mood', 'unknown')

            if mood is None or mood == '':
                mood = 'unknown'
            
            MoodRecord.objects.create(user=request.user, mood_rating=mood)
            return JsonResponse({'mood': mood})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@login_required
def view_feedback(request):
    mood_records = MoodRecord.objects.filter(user=request.user).order_by('timestamp')
    serialized_records = json.dumps(list(mood_records.values()), cls=DjangoJSONEncoder)
    context = {
        'mood_records': serialized_records
    }
    return render(request, 'view_feedback.html', context)

@login_required
def view_statistics(request):
    return render(request, 'view_statistics.html')

@login_required
def view_settings(request):
    return render(request, 'view_settings.html')

@login_required
def show_symptom_selection(request):
    if request.method == 'POST':
        forms = [
            ('hallucinations', HallucinationsForm(request.POST, prefix='hallucinations')),
            ('flattening', FlatteningForm(request.POST, prefix='flattening')),
            ('avolition', AvolitionForm(request.POST, prefix='avolition')),
            ('difficulty_concentrating', DifficultyConcentratingForm(request.POST, prefix='difficulty_concentrating')),
            ('social_cognition', SocialCognitionForm(request.POST, prefix='social_cognition'))
        ]

        for symptom_type, form in forms:
            if form.is_valid():
                instance = form.save(commit=False)
                instance.symptom_type = symptom_type
                instance.user = request.user
                # Collect MCQ answers
                mcq_answers = {}
                for field_name in form.cleaned_data:
                    if field_name.startswith(f'{symptom_type}_q'):
                        mcq_answers[field_name] = form.cleaned_data[field_name]
                print(f"MCQ Answers for {symptom_type}: {mcq_answers}")  # Debug statement
                instance.mcq_answers = json.dumps(mcq_answers)
                instance.save()
            else:
                print(f"Form is invalid for {symptom_type}: {form.errors}")

        return HttpResponseRedirect(reverse('view_symptoms'))

    else:
        forms = {
            'hallucinations_form': HallucinationsForm(prefix='hallucinations'),
            'flattening_form': FlatteningForm(prefix='flattening'),
            'avolition_form': AvolitionForm(prefix='avolition'),
            'difficulty_concentrating_form': DifficultyConcentratingForm(prefix='difficulty_concentrating'),
            'social_cognition_form': SocialCognitionForm(prefix='social_cognition')
        }
    return render(request, 'select_symptom.html', forms)

@login_required
def view_symptoms(request):
    symptom_records = SymptomRecord.objects.filter(user=request.user).order_by('timestamp')
    for record in symptom_records:
        record.mcq_answers = json.loads(record.mcq_answers)
        print(f"MCQ Answers for {record.symptom_type}: {record.mcq_answers}")  # Debug statement
    context = {
        'symptom_records': symptom_records,
        'hallucinations_q1_choices': {"A": "Frequently", "B": "Occasionally", "C": "Rarely", "D": "Never"},
        'hallucinations_q2_choices': {"A": "Yes, frequently", "B": "Yes, a few times", "C": "Yes, once", "D": "No, never"},
        'hallucinations_q3_choices': {"A": "Yes, always", "B": "Yes, sometimes", "C": "Yes, but rarely", "D": "No, never"},
        'hallucinations_q4_choices': {"A": "Often", "B": "Occasionally", "C": "Seldom", "D": "Never"},
        'flattening_q1_choices': {"A": "Very often", "B": "Sometimes", "C": "Rarely", "D": "Never"},
        'flattening_q2_choices': {"A": "Frequently", "B": "Occasionally", "C": "Rarely", "D": "Never"},
        'flattening_q3_choices': {"A": "Very frequently", "B": "Often", "C": "Sometimes", "D": "Never"},
        'flattening_q4_choices': {"A": "Yes, very often", "B": "Yes, sometimes", "C": "Yes, but rarely", "D": "No, never"},
        'avolition_q1_choices': {"A": "Very often", "B": "Often", "C": "Sometimes", "D": "Never"},
        'avolition_q2_choices': {"A": "Almost always", "B": "Frequently", "C": "Occasionally", "D": "Never"},
        'difficulty_concentrating_q1_choices': {"A": "Very often", "B": "Often", "C": "Sometimes", "D": "Never"},
        'difficulty_concentrating_q2_choices': {"A": "Always", "B": "Often", "C": "Sometimes", "D": "Never"},
        'difficulty_concentrating_q3_choices': {"A": "Very frequently", "B": "Often", "C": "Occasionally", "D": "Never"},
        'difficulty_concentrating_q4_choices': {"A": "Very often", "B": "Often", "C": "Sometimes", "D": "Never"},
        'difficulty_concentrating_q5_choices': {"A": "Very frequently", "B": "Often", "C": "Sometimes", "D": "Never"},
        'difficulty_concentrating_q6_choices': {"A": "Almost always", "B": "Often", "C": "Occasionally", "D": "Never"},
        'social_cognition_q1_choices': {"A": "Very often", "B": "Often", "C": "Sometimes", "D": "Never"},
        'social_cognition_q2_choices': {"A": "Very frequently", "B": "Often", "C": "Occasionally", "D": "Never"},
    }
    return render(request, 'view_symptoms.html', context)

@csrf_exempt
@login_required
def record_symptom(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            symptoms_data = data.get('symptoms', {})

            for symptom_type, details in symptoms_data.items():
                description = details.get('description', '')
                severity = details.get('severity', 0)
                mcq_answers = details.get('mcq_answers', {})

                symptom = SymptomRecord.objects.create(
                    user=request.user,
                    symptom_type=symptom_type,
                    description=description,
                    severity=severity,
                    mcq_answers=mcq_answers
                )
                symptom.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
