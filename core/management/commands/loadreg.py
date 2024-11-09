import csv
from django.core.management.base import BaseCommand, CommandParser
from core.models import Course, Section, Registration, Student

class Command(BaseCommand):

    help = 'Load registration from Examination List Report'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('input_file', type=str, help='Path to the input file (examination list)')
        parser.add_argument('output_file', type=str, help='Path to the output CSV file')
    
    def handle(self, *args, **kwargs) -> str | None:
        input_file = kwargs['input_file']
        output_file = kwargs['output_file']

        with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
            reader = csv.DictReader(infile)

            fieldnames = ['student id', 'student name', 'course id', 'course name', 'section']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)

            # write the header
            if outfile.tell() == 0:
                writer.writeheader()

            for row in reader:

                try:

                    student_id = row['Student No']
                    student = Student.objects.get(username=student_id)

                    course_id = row['Course No']
                    course = Course.objects.get(code=course_id)

                    section_no = int(row['Section No'].strip())
                    section = Section.objects.get(course=course, number=section_no)

                    Registration.objects.get_or_create(
                        student=student, 
                        section=section)
                    
                    # 'student id', 'student name', 'course id', 'course name', 'section'
                    writer.writerow({'student id': student.username, 
                                     'student name': str(student), 
                                     'course id': course.code, 
                                     'course name': course.name, 
                                     'section': section.number})

                except (Student.DoesNotExist, Course.DoesNotExist, Section.DoesNotExist):
                    self.stdout.write(f"Skipping record: Missing data for student {student_id}, course {course_id} or section {section_no}")