class StudentResultManager:
    """Manage student exam results and perform analysis operations."""

    def __init__(self):
        """Initialize student results dictionary with sample data."""
        self.students = {
            "S001": {"name": "Arjun", "math": 85, "science": 92, "english": 78},
            "S002": {"name": "Nisha", "math": 95, "science": 88, "english": 90},
            "S003": {"name": "Rohan", "math": 72, "science": 79, "english": 85},
            "S004": {"name": "Divya", "math": 88, "science": 95, "english": 92},
            "S005": {"name": "Karan", "math": 80, "science": 82, "english": 88}
        }

    def calculate_student_averages(self):
        """
        Calculate and print average score for each student across all subjects.
                Output:
            - Print: "Student Averages: {dictionary with student_id: average}"
        """



    def find_highest_average(self):
        """
        Find and print the student with the highest average score.
        Output:
            - Print: "Highest Average: {name} ({student_id}) - {average}"
        """

    def calculate_subject_averages(self):
        """
        Calculate and print average score for each subject across all students.
        Output:
            - Print: "Subject Averages: {dictionary with subject: average}"
        """

