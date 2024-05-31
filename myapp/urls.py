# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_mood_selection, name='show_mood_selection'),
    path('record_mood/', views.record_mood, name='record_mood'),
    path('view_feedback/', views.view_feedback, name='view_feedback'),
    path('view_statistics/', views.view_statistics, name='view_statistics'),
    path('view_settings/', views.view_settings, name='view_settings'),
    path('select_symptom/', views.show_symptom_selection, name='show_symptom_selection'),
    path('record_symptom/', views.record_symptom, name='record_symptom'),
    path('view_symptoms/', views.view_symptoms, name='view_symptoms'),
]
