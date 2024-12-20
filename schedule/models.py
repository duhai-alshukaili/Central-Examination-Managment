from django.db import models
from django.contrib.auth import get_user_model
from core.models import Room, Section

User = get_user_model()

class Schedule(models.Model):
    # Foreign Key to the Room model
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    # Foreign Key to the Section model (sectionID)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    # Exam Date
    examDate = models.DateField()

    # Exam Time (in 24-hour format)
    examTime = models.TimeField()

    # Duration of the exam in minutes
    duration = models.PositiveBigIntegerField(help_text="Duration of the exam in minutes")

    def __str__(self):
        # Directly access related objects through foreign key fields
        course = self.section.course
        section_number = self.section.number

        # Return a readable string representation of the schedule
        return f"Schedule for {course.code} - {course.name} (Section {section_number}) on {self.examDate} at {self.examTime}"

class Invigilation(models.Model):

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    
    # Exam Date
    examDate = models.DateField()

    # Exam Time (in 24-hour format)
    examTime = models.TimeField()

    invigilator = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('room', 'examDate', 'examTime', 'invigilator')
    
    def __str__(self):
        return f"Invigilation: {self.invigilator} in {self.room} on {self.examDate} at {self.examTime}"




