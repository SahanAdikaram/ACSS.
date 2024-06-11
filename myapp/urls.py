from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),  # Landing page
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('select_mood/', views.show_mood_selection, name='select_mood'),
    path('record_mood/', views.record_mood, name='record_mood'),
    path('view_feedback/', views.view_feedback, name='view_feedback'),
    path('view_statistics/', views.view_statistics, name='view_statistics'),
    path('view_settings/', views.view_settings, name='view_settings'),
    path('select_symptom/', views.show_symptom_selection, name='select_symptom'),
    path('view_symptoms/', views.view_symptoms, name='view_symptoms'),
    path('record_symptom/', views.record_symptom, name='record_symptom'),
]
