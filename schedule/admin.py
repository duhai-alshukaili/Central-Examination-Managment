from django.contrib import admin
from .models import Schedule, Invigilation

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('section', 'room', 'examDate', 'examTime', 'duration')
    list_filter = ('room', 'section', 'examDate')
    search_fields = ('section__course__name', 'room__label')


@admin.register(Invigilation)
class InvigilationAdmin(admin.ModelAdmin):
    list_display = ('room', 'examDate', 'examTime', 'invigilator')
    list_filter = ('room','examDate', 'invigilator')
    search_fields = ('room__label', 'invigilator__username')
