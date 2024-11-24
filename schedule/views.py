from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from schedule.models import Schedule, Invigilation
from core.models import Registration, Student, Lecturer, User, Section

class ExamScheduleView(LoginRequiredMixin, ListView):
    model = Schedule
    template_name = 'schedule/exam_schedule.html'
    context_object_name = 'exam_schedule'

    def get_queryset(self):
        
        # Get the user
        user = self.request.user

        # Ensure that the user is a student
        if user.user_type == User.STUDENT:

            # get the student object
            student = Student.objects.filter(username=self.request.user.username).first()

            # Get the sections the student is registred for
            sections = Registration.objects.filter(student=student).values_list('section', flat=True)

            # Filter the schdule for the student's registred sections
            return Schedule.objects.filter(section__in=sections).order_by('examDate', 'examTime')
        elif user.user_type == User.ACADEMIC_STAFF:

            # get the lecturer object
            lecturer = Lecturer.objects.filter(username=self.request.user.username).first()

            # Get the section the lecturer is teaching
            sections = Section.objects.filter(lecturer=lecturer).values_list('id', flat=True)

            # Filter the schdule for the sections taught by the lecturer
            return Schedule.objects.filter(section__in=sections).order_by('examDate', 'examTime',  'section__number')

        
        return Schedule.objects.none() # Return empty queryset if the user is not a student
    
class InvigilationView(LoginRequiredMixin, ListView):
    model = Invigilation
    template_name = 'schedule/invigilation.html'
    context_object_name = 'invigilations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invigilations = self.get_queryset()
        schedule_data = []

        # Fetch releated schdule detauls
        for invigilation in invigilations:
            schedules = Schedule.objects.filter(
                room=invigilation.room,
                examDate=invigilation.examDate, 
                examTime=invigilation.examTime,
            )

            print(schedules)

            for schedule in schedules:
                schedule_data.append({
                    'room': invigilation.room,
                    'exam_date': invigilation.examDate,
                    'exam_time': invigilation.examTime,
                    'course_id': schedule.section.course.code,
                    'course_name': schedule.section.course.name,
                    'section_number': schedule.section.number,
                })
            
            context['invigilations'] = schedule_data
            return context
            
    
    def get_queryset(self):
        
        # Get the user
        user = self.request.user

        # Ensure that the user is a lecturer
        if user.user_type == User.ACADEMIC_STAFF:

            # print some debug information here
            print("User is a lecturer")
            print(user.username)

            # Filter the invigilation for the lecturer
            return Invigilation.objects.filter(invigilator=user).order_by('examDate', 'examTime')
        
        return Invigilation.objects.none() # Return empty queryset if the user is not a lecturer
