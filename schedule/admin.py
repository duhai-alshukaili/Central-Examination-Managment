from django.contrib import admin
from .models import Schedule

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('sectionID', 'roomID', 'examDate', 'examTime', 'duration')
    list_filter = ('roomID', 'sectionID', 'examDate')
    search_fields = ('sectionID__course__name', 'roomID__label')