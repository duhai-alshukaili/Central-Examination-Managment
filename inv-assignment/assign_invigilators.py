import csv
import random
from itertools import cycle

def load_faculty_ids(faculty_file):
    """Load faculty IDs from a text file."""
    with open(faculty_file, 'r') as file:
        faculty_ids = [line.strip() for line in file.readlines() if line.strip()]
    return faculty_ids

def assign_invigilators(schedule_file, faculty_file, output_file):
    """Assign invigilators to rooms and save the output."""
    # Load faculty IDs
    faculty_ids = load_faculty_ids(faculty_file)
    random.shuffle(faculty_ids)

    if len(faculty_ids) < 2:
        raise ValueError("At least two faculty IDs are required for invigilation.")

    # Use a cycle to ensure uniform assignment
    faculty_cycle = cycle(faculty_ids)

    # Open the schedule file and the output file
    with open(schedule_file, 'r') as schedule_csv, open(output_file, 'w', newline='') as output_csv:
        reader = csv.DictReader(schedule_csv)
        fieldnames = reader.fieldnames + ['Invigilator 1', 'Invigilator 2']
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)

        # Write header to the output file
        writer.writeheader()

        # Process each record in the schedule
        for row in reader:
            # Assign two invigilators
            row['Invigilator 1'] = next(faculty_cycle)
            row['Invigilator 2'] = next(faculty_cycle)

            # Write the updated row to the output file
            writer.writerow(row)

    print(f"Invigilator assignments saved to {output_file}")

if __name__ == "__main__":
    # Input files
    schedule_file = 'schedule.csv'  # Replace with your schedule file path
    faculty_file = 'faculty_ids.txt'  # Replace with your faculty list file path

    # Output file
    output_file = 'schedule_with_invigilators.csv'

    # Assign invigilators
    try:
        assign_invigilators(schedule_file, faculty_file, output_file)
    except Exception as e:
        print(f"Error: {e}")
