from django.contrib import admin
from .models import Schedule

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('section', 'room', 'examDate', 'examTime', 'duration')
    list_filter = ('room', 'section', 'examDate')
    search_fields = ('section__course__name', 'room__label')