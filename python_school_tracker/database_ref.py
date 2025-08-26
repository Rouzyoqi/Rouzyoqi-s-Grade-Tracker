import json
import os
from statistics import mean

SUBJECTS_FILE = "subjects.json"

def load_subjects():
    """Load list of subjects."""
    if not os.path.exists(SUBJECTS_FILE):
        return []
    with open(SUBJECTS_FILE, "r") as f:
        return json.load(f)

def save_subjects(subjects):
    """Save list of subjects."""
    with open(SUBJECTS_FILE, "w") as f:
        json.dump(subjects, f, indent=4)

def add_subject(subject):
    """Add a new subject (creates a JSON file)."""
    subjects = load_subjects()
    if subject not in subjects:
        subjects.append(subject)
        save_subjects(subjects)

        # Create a new subject JSON file
        with open(f"{subject}.json", "w") as f:
            json.dump({}, f, indent=4)

def load_grades(subject):
    """Load grades for a given subject."""
    try:
        with open(f"{subject}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_grades(subject, grades):
    """Save grades for a given subject."""
    with open(f"{subject}.json", "w") as f:
        json.dump(grades, f, indent=4)

def add_grade(subject, assignment, grade):
    """Add a grade to a subject’s JSON file."""
    grades = load_grades(subject)
    grades[assignment] = grade
    save_grades(subject, grades)

def get_stats(subject):
    """Return a string with stats for one subject."""
    grades = load_grades(subject)
    if not grades:
        return "No grades yet.\n"

    text_output = ""
    subject_grades = []

    for assignment, grade in grades.items():
        text_output += f"{assignment}: {grade}\n"
        subject_grades.append(grade)

    if subject_grades:
        text_output += f"\nAverage: {mean(subject_grades):.2f}"

    return text_output

def clear_all():
    """Delete all subjects and their JSON files."""
    subjects = load_subjects()
    for subject in subjects:
        filename = f"{subject}.json"
        if os.path.exists(filename):
            os.remove(filename)
    if os.path.exists(SUBJECTS_FILE):
        os.remove(SUBJECTS_FILE)
