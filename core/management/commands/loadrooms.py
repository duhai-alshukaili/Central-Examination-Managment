from django.core.management.base import BaseCommand
import csv
from pathlib import Path
from django.db import transaction
from core.models import Room  # Adjust the import path based on your app name

class Command(BaseCommand):
    help = 'Load rooms from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def get_room_type(self, type_str):
        """Convert room type string to corresponding model value"""
        type_mapping = {
            'classroom': Room.CLASS_ROOM,
            'computer lab': Room.COMPUTER_LAB,
            'physics lab': Room.PHYSICS_LAB,
            'chemistry lab': Room.CHEMISTRY_LAB,
            'cad workshop': Room.CAD_WORKSHOP,
            'lecture hall': Room.LECTURE_HALL,
        }
        return type_mapping.get(type_str.lower(), Room.CLASS_ROOM)

    def get_campus_code(self, campus_str):
        """Convert campus string to corresponding model value"""
        campus_mapping = {
            'al saada': Room.SA,
            'al akhdar': Room.AK,
            'sa': Room.SA,
            'ak': Room.AK,
        }
        return campus_mapping.get(campus_str.lower())

    def extract_block(self, room_label):
        """Extract block from room label (assuming format like 'B1-1.01')"""
        if '-' in room_label:
            return room_label.split('-')[0]
        return room_label[0]  # Fallback to first character if no hyphen

    def handle(self, *args, **options):
        csv_path = Path(options['csv_file'])
        if not csv_path.exists():
            self.stderr.write(self.style.ERROR(f'File {csv_path} does not exist'))
            return

        successful_imports = 0
        failed_imports = 0
        error_records = []

        try:
            with csv_path.open() as csv_file:
                reader = csv.DictReader(csv_file)
                
                # Validate CSV headers
                required_headers = {'campus', 'room', 'type', 'capacity'}
                if not required_headers.issubset(set(reader.fieldnames)):
                    self.stderr.write(
                        self.style.ERROR('CSV file missing required headers. '
                                       f'Required: {required_headers}')
                    )
                    return

                # Process records within a transaction
                with transaction.atomic():
                    for row_number, row in enumerate(reader, start=2):  # Start at 2 to account for header row
                        try:
                            # Convert and validate campus
                            campus_code = self.get_campus_code(row['campus'])
                            if not campus_code:
                                raise ValueError(f"Invalid campus: {row['campus']}")

                            # Convert and validate room type
                            room_type = self.get_room_type(row['type'])

                            # Convert capacity to integer
                            try:
                                capacity = int(row['capacity'])
                                if capacity <= 0:
                                    raise ValueError
                            except (ValueError, TypeError):
                                raise ValueError(f"Invalid capacity: {row['capacity']}")

                            # Extract block from room label
                            block = self.extract_block(row['room'])

                            # Create or update room
                            room, created = Room.objects.update_or_create(
                                label=row['room'],
                                campus=campus_code,
                                defaults={
                                    'room_type': room_type,
                                    'capacity': capacity,
                                    'block': block,
                                }
                            )

                            successful_imports += 1

                        except Exception as e:
                            failed_imports += 1
                            error_records.append(f"Row {row_number}: {str(e)}")

        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f'Failed to process CSV file: {str(e)}')
            )
            return

        # Print summary
        self.stdout.write(self.style.SUCCESS(
            f'Successfully imported {successful_imports} rooms'
        ))
        
        if failed_imports:
            self.stdout.write(self.style.WARNING(
                f'Failed to import {failed_imports} rooms'
            ))
            self.stdout.write(self.style.WARNING('Errors:'))
            for error in error_records:
                self.stdout.write(self.style.WARNING(error))