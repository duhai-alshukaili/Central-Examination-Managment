import csv
from django.core.management.base import BaseCommand
from schedule.models import Invigilation, Schedule
from core.models import Room, User

class Command(BaseCommand):

    help = 'Load invigilations from file'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path', type=str, help="Path to the schedule csv file"
        )
    
    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        records_skipped = 0
        records_added = 0

        try:
            with open(file_path, 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    # Room Number,Campus,Exam Date,Exam Time,Invigilator 1,Invigilator 2
                    room_label = row["Room Number"]
                    campus     = row["Campus"]
                    exam_date  = row["Exam Date"]
                    exam_time  = row["Exam Time"]
                    invigilator_ids = [row["Invigilator 1"], row["Invigilator 2"]]

                    # Get room object
                    room = Room.objects.filter(label=room_label, campus=campus).first()
                    if not room:
                        self.stdout.write(f"Room {room_label} in campus {campus} not found. Skipping record.")
                        records_skipped += 1
                        continue

                    # Check if a schedule exists for the given room, date, and time
                    schedule_exists = Schedule.objects.filter(
                        room = room,
                        examDate=exam_date,
                        examTime=exam_time
                    ).exists()

                    if not schedule_exists:
                        self.stdout.write(
                             f"No schedule found for room {room_label}, campus {campus} on {exam_date} at {exam_time}. Skipping record."
                        )
                        records_skipped += 1
                        continue

                    # Assign invigilators
                    for inv_id in invigilator_ids:
                        invigilator = User.objects.filter(username=inv_id).first()
                        if not invigilator:
                            self.stdout.write(f"Invigilator {inv_id} not found. Skipping.")
                            records_skipped += 1
                            continue
                    
                        # cehck if an invigilatoin record already exists
                        _, created = Invigilation.objects.get_or_create(
                            room=room,
                            examDate=exam_date,
                            examTime=exam_time,
                            invigilator=invigilator
                        )
                        if created:
                            records_added += 1


        except FileNotFoundError:
            self.stdout.write(f"File {file_path} not found.")
        
        self.stdout.write(f"Invigilation data loading complete.")
        self.stdout.write(f"Records added: {records_added}")
        self.stdout.write(f"Records skipped: {records_skipped}")