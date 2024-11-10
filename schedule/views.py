from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from schedule.models import Schedule
from core.models import Registration, Student

class ExamScheduleView(LoginRequiredMixin, ListView):
    model = Schedule
    template_name = 'schedule/exam_schedule.html'
    context_object_name = 'exam_schedule'

    def get_queryset(self):
        
        # Get the user
        user = self.request.user

        # Ensure that the user is a student
        if user.user_type == 'student':

            # get the student object
            student = Student.objects.filter(username=self.request.user.username).first()

            # Get the sections the student is registred for
            sections = Registration.objects.filter(student=student).values_list('section', flat=True)

            # Filter the schdule for the student's registred sections
            return Schedule.objects.filter(sectionID__in=sections).order_by('examDate', 'examTime')
        
        return Schedule.objects.none() # Return empty queryset if the user is not a student
