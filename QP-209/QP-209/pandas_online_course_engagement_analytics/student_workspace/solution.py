# student_workspace/solution.py

import pandas as pd


class CourseEngagementAnalytics:
    """Analytics helper for online course engagement using Pandas."""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy() if df is not None else pd.DataFrame()

    def completion_percentage(self) -> dict:
        """Return completion percentage per student-course as dict 'S-C': pct"""
        if self.df is None or self.df.empty:
            return {}
        df = self.df.copy()
        df['completion_pct'] = (df['completed_modules'] / df['total_modules'] * 100).round(1)
        result = {f"{r['student_id']}-{r['course_id']}": float(r['completion_pct']) for _, r in df.iterrows()}
        return result

    def most_engaged_course(self) -> str:
        """Return the course_id with highest total watch_minutes."""
        if self.df is None or self.df.empty:
            return None
        agg = self.df.groupby('course_id', dropna=False)['watch_minutes'].sum()
        return agg.idxmax()

    def inactive_students(self, threshold: int = 7) -> list:
        """Return sorted list of student_ids with last_active_days > threshold."""
        if self.df is None or self.df.empty:
            return []
        inactive = self.df[self.df['last_active_days'] > threshold]['student_id'].unique().tolist()
        return sorted(inactive)

    def duplicate_records(self) -> int:
        """Return count of duplicate records based on student_id+course_id+watch_minutes."""
        if self.df is None or self.df.empty:
            return 0
        dup = int(self.df.duplicated(subset=['student_id', 'course_id', 'watch_minutes'], keep='first').sum())
        return dup

    def rank_students(self, top_n: int = 3) -> list:
        """Return list of top N student_ids ranked by total watch_minutes desc."""
        if self.df is None or self.df.empty:
            return []
        agg = self.df.groupby('student_id')['watch_minutes'].sum().sort_values(ascending=False)
        return agg.index.tolist()[:top_n]


# Convenience standalone functions (visible API used by tests)
def completion_percentage(df):
    return CourseEngagementAnalytics(df).completion_percentage()


def most_engaged_course(df):
    return CourseEngagementAnalytics(df).most_engaged_course()


def inactive_students(df):
    return CourseEngagementAnalytics(df).inactive_students()


def duplicate_records(df):
    return CourseEngagementAnalytics(df).duplicate_records()


def rank_students(df):
    return CourseEngagementAnalytics(df).rank_students()
