class EmployeeManager:
    """Manage employee dictionary and perform operations."""

    def __init__(self):
        """Initialize employee dictionary with sample data."""
        self.employees = {
            "E001": {"name": "Raj", "department": "IT", "salary": 50000},
            "E002": {"name": "Priya", "department": "HR", "salary": 45000},
            "E003": {"name": "Amit", "department": "IT", "salary": 55000},
            "E004": {"name": "Sara", "department": "Finance", "salary": 48000},
            "E005": {"name": "Vikram", "department": "IT", "salary": 60000}
        }

    def calculate_average_it_salary(self):
        """
        Calculate and print average salary of IT department employees.
        
        Processing:
            - Filter employees by department == "IT"
            - Calculate average: total_salary / count
        Output:
            - Print: "Average IT Salary: {average}"
        """
        it_employees = [emp for emp in self.employees.values() if emp["department"] == "IT"]
        """Your code here"""
    def find_highest_paid_employee(self):
        """
        Find and print the highest paid employee across all departments.
        
        Processing:
            - Iterate through all employees
            - Track employee with maximum salary
        Output:
            - Print: "Highest Paid Employee: {name} ({emp_id}) - {salary}"
        """
        if self.employees:
            highest_emp_id = None
            highest_salary = -1
            
            """Your code here"""
                print(f"Highest Paid Employee: {emp_name} ({highest_emp_id}) - {highest_salary}")
        else:
            print("No employees found")

    def check_employee(self, emp_id):
        """
        Check if employee exists by ID and display details.
        
        Parameters:
            emp_id (str): Employee ID to search for (e.g., "E002")
        Output:
            - If found: "Employee {emp_id}: {name} - {salary}"
            - If not found: "Employee {emp_id} not found"
        """
        if emp_id in self.employees:
            """Your code here"""

