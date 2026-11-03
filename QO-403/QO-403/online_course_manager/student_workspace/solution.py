class CourseManager:
    """Manage online courses and student registrations."""

    def __init__(self):
        """Initialize the course manager with an empty courses dictionary."""
        """Your code here"""

    def add_course(self, course_id: str, title: str, capacity: int) -> None:
        """
        Add a new course to the manager.
        
        Parameters:
            course_id (str): Unique course identifier
            title (str): Course title/name
            capacity (int): Maximum number of students allowed
        
        Returns:
            None
        """
        """Your code here"""
    def register_student(self, course_id: str, name: str) -> str:
        """
        Register a student to a course with capacity validation.
        
        Parameters:
            course_id (str): Course identifier
            name (str): Student name
        
        Returns:
            str: "Invalid ID" if course doesn't exist
                 "Course Full" if at capacity
                 "Enrolled in [title]" if successful
        """
        """Your  code  here"""
        
        course = self.courses[course_id]
        
        """Your code here"""

    def get_available_seats(self, course_id: str) -> int:
        """
        Calculate available seats in a course.
        
        Parameters:
            course_id (str): Course identifier
        
        Returns:
            int: Number of available seats if course exists
                 -1 if course doesn't exist
        """
        """Your code here"""

    def remove_student(self, course_id: str, name: str) -> str:
        """
        Remove a student from a course.
        
        Parameters:
            course_id (str): Course identifier
            name (str): Student name
        
        Returns:
            str: "Removed [name] from [title]" if successful
                 "Registration not found" if course/student doesn't exist
        """
        """Your code here"""
        
        course = self.courses[course_id]
        
        """Your code here"""

