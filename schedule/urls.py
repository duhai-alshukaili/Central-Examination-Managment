from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name='schedule'

urlpatterns = [
    path('', views.ExamScheduleView.as_view(), name='list'),
    path('invigilation/', views.InvigilationView.as_view(), name='invigilation'),
]