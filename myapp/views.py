import base64
import json
import io
from pydub import AudioSegment
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.core.serializers.json import DjangoJSONEncoder
from django.core.files.base import ContentFile
from .models import MoodRecord, SymptomRecord
from .forms import SymptomForm

def show_mood_selection(request):
    return render(request, 'select_mood.html')

@csrf_exempt
def record_mood(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mood = data.get('mood', 'unknown')

            if mood is None or mood == '':
                mood = 'unknown'
            
            MoodRecord.objects.create(mood_rating=mood)
            return JsonResponse({'mood': mood})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

def view_feedback(request):
    mood_records = MoodRecord.objects.all().order_by('timestamp')
    serialized_records = json.dumps(list(mood_records.values()), cls=DjangoJSONEncoder)
    context = {
        'mood_records': serialized_records
    }
    return render(request, 'view_feedback.html', context)

def view_statistics(request):
    return render(request, 'view_statistics.html')

def view_settings(request):
    return render(request, 'view_settings.html')

def show_symptom_selection(request):
    if request.method == 'POST':
        print("POST data received:", request.POST)
        form = SymptomForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid")
            symptom = form.save(commit=False)
            if 'photo_data' in request.POST and request.POST['photo_data']:
                format, imgstr = request.POST['photo_data'].split(';base64,')
                ext = format.split('/')[-1]
                symptom.photo = ContentFile(base64.b64decode(imgstr), name=f'{symptom.id}_photo.{ext}')
            if 'audio_data' in request.POST and request.POST['audio_data']:
                format, audstr = request.POST['audio_data'].split(';base64,')
                ext = format.split('/')[-1]
                audio_data = base64.b64decode(audstr)
                symptom.voice_record = ContentFile(audio_data, name=f'{symptom.id}_audio.mp3')
            symptom.save()
            print("Symptom saved:", symptom)
            return redirect('view_symptoms')
        else:
            print("Form is invalid", form.errors)
    else:
        form = SymptomForm()
    return render(request, 'select_symptom.html', {'form': form})

@csrf_exempt
def record_symptom(request):
    if request.method == 'POST':
        try:
            description = request.POST.get('description', '')
            severity = request.POST.get('severity', 0)
            symptom_type = request.POST.get('symptom_type', 'unknown')
            multiple_choice = request.POST.get('multiple_choice', '')
            photo_data = request.POST.get('photo_data', None)
            audio_data = request.POST.get('audio_data', None)

            symptom = SymptomRecord.objects.create(
                symptom_type=symptom_type,
                description=description,
                severity=severity,
                multiple_choice=multiple_choice,
            )

            if photo_data:
                format, imgstr = photo_data.split(';base64,')
                ext = format.split('/')[-1]
                photo = ContentFile(base64.b64decode(imgstr), name=f'{symptom.id}_photo.{ext}')
                symptom.photo = photo

            if audio_data:
                format, audiostr = audio_data.split(';base64,')
                ext = format.split('/')[-1]
                audio_data = base64.b64decode(audiostr)
                # Convert WebM to MP3
                audio = AudioSegment.from_file(io.BytesIO(audio_data), format="webm")
                mp3_data = io.BytesIO()
                audio.export(mp3_data, format="mp3")
                symptom.voice_record = ContentFile(mp3_data.getvalue(), name=f'{symptom.id}_audio.mp3')
                
            symptom.save()

            return JsonResponse({'symptom': symptom_type})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

def view_symptoms(request):
    symptom_records = SymptomRecord.objects.all().order_by('timestamp')
    context = {
        'symptom_records': symptom_records
    }
    return render(request, 'view_symptoms.html', context)
