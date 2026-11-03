# student_workspace/solution.py

import pandas as pd

class HRAnalytics:

    def load_data(self, emp_path: str, att_path: str) -> tuple:
        """Load employee and attendance CSV files"""
        employees_df = pd.read_csv(emp_path)
        attendance_df = pd.read_csv(att_path)
        attendance_df["login_time"] = pd.to_datetime(attendance_df["login_time"])
        attendance_df["logout_time"] = pd.to_datetime(attendance_df["logout_time"])
        return employees_df, attendance_df

    def total_working_hours(self, attendance_df: pd.DataFrame) -> dict:
        """Calculate total working hours for each employee"""
        attendance_df["duration"] = (attendance_df["logout_time"] - attendance_df["login_time"]).dt.total_seconds() / 3600
        total_hours = attendance_df.groupby("emp_id")["duration"].sum().round(2).to_dict()
        return total_hours

    def late_joiners(self, attendance_df: pd.DataFrame) -> list:
        """Return employees who logged in after 10:00 AM"""
        late_df = attendance_df[attendance_df["login_time"].dt.time > pd.to_datetime("10:00:00").time()]
        return sorted(late_df["emp_id"].unique().tolist())

    def absentees(self, employees_df: pd.DataFrame, attendance_df: pd.DataFrame) -> list:
        """Return employees who never logged in"""
        emp_all = set(employees_df["emp_id"])
        emp_present = set(attendance_df["emp_id"])
        absent = sorted(emp_all - emp_present)
        return absent
