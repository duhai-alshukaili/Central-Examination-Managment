import re
import csv
from datetime import datetime, timedelta
from django.conf import settings
from core.models import Room, Section, Course
from schedule.models import Schedule
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Extracts schedule data from a timetable file and saves it to the database and a CSV file.'

    def add_arguments(self, parser):
        parser.add_argument('input_file', type=str, help='Path to the input file (timetable)')
        parser.add_argument('output_file', type=str, help='Path to the output CSV file')

    def handle(self, *args, **kwargs):
        input_file = kwargs['input_file']
        output_file = kwargs['output_file']
        
        with open(input_file, 'r') as file, open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write CSV header
            writer.writerow(["Course Code", "Course Name", "Exam Date", "Exam Time", "Exam Duration", "Campus", "Room Number", "Section Number"])
            
            exam_date = None
            course_code = None
            course_name = None
            exam_time = None
            exam_duration = None
            
            for line in file:
                line = line.strip()
                
                # Check for exam date line
                if "Exam Schedule on" in line:
                    exam_date = self.parse_exam_date(line)
                
                # Check for course info line
                elif " -- " in line and not line.startswith("Exam"):
                    course_code, course_name = self.parse_course_info(line)
                    
                # Check for time line
                elif re.match(r'^\d{1,2}.*to.*', line):
                    exam_time, exam_duration = self.parse_time_and_duration(line)
                    
                # Check for section info line
                elif re.match(r'^\d+\s+\S+_\S+\s+\d+', line):
                    campus, room, section = self.parse_section(line)
                    
                    # Write a row for each section entry
                    if all([exam_date, course_code, course_name, exam_time, exam_duration, campus, room, section]):
                        # Save to CSV
                        writer.writerow([
                            course_code, course_name, exam_date,
                            exam_time.strftime("%H:%M"), exam_duration, campus, room, section
                        ])

                        # Save to the database
                        self.save_schedule_record(course_code, course_name, exam_date, exam_time, exam_duration, campus, room, section)

    def parse_exam_date(self, line):
        match = re.search(r'(\d{2})-(\w{3})-(\d{4})', line)
        if match:
            return datetime.strptime(match.group(0), '%d-%b-%Y').date()
        return None

    def parse_course_info(self, line):
        match = re.match(r'^(\S+)\s--\s(.+)', line)
        if match:
            return match.group(1).strip(), match.group(2).strip()
        return None, None
    
    def parse_time_and_duration(self, line):
        # Single regex pattern to match all time formats
        match = re.match(r"(\d{1,2})([:.]\d{2})?\s*([APap]\.?[Mm])\s+to\s+(\d{1,2})([:.]\d{2})?\s*([APap]\.?[Mm])", line)
        
        if match:
            start_hour = int(match.group(1))
            start_minute = int(match.group(2)[1:]) if match.group(2) else 0
            start_period = match.group(3).replace('.', '').upper()  # Remove any period for consistency
            
            end_hour = int(match.group(4))
            end_minute = int(match.group(5)[1:]) if match.group(5) else 0
            end_period = match.group(6).replace('.', '').upper()  # Remove any period for consistency

            # Convert start and end times to 24-hour format
            start_time = datetime.strptime(f"{start_hour:02}:{start_minute:02} {start_period}", "%I:%M %p").time()
            end_time = datetime.strptime(f"{end_hour:02}:{end_minute:02} {end_period}", "%I:%M %p").time()

            # Calculate duration in minutes
            duration = int((datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)).total_seconds() / 60)

            return start_time, duration

        # Return None if the pattern does not match
        return None, None

    def parse_section(self, line):
        parts = line.split()
        if len(parts) >= 4:
            campus_room = parts[1]
            section = parts[2]
            campus = campus_room.split('_')[0][:2]
            room = campus_room.split('_')[1] if '_' in campus_room else ""
            return campus, room, section
        return None, None, None

    def save_schedule_record(self, course_code, course_name, exam_date, exam_time, exam_duration, campus, room, section_number):
        try:
            course = Course.objects.get(code=course_code, name=course_name)
            room = Room.objects.get(campus=campus, label=room)
            section = Section.objects.get(course=course, number=section_number)
            
            Schedule.objects.get_or_create(
                roomID=room,
                sectionID=section,
                examDate=exam_date,
                examTime=exam_time,
                duration=exam_duration
            )
        except (Course.DoesNotExist, Room.DoesNotExist, Section.DoesNotExist):
            self.stdout.write(f"Skipping record: Missing data for course {course_name}, room {room} or section {section_number}")
