import pandas as pd

class StudentTracker:
    """
    Academic Performance Management System using Pandas.
    
    This class manages student academic records using a Pandas DataFrame.
    It allows you to:
    - Store student names, scores, and subjects
    - Calculate averages for specific subjects
    - Find top performers above a threshold
    - Get summary statistics
    
    Key Concept: Use self.data as a DataFrame with columns:
    ['StudentName', 'Score', 'Subject']
    """

    def __init__(self):
        """
        Initialize an empty DataFrame with student performance records.
        
        Implementation Guide:
        - Create an empty Pandas DataFrame
        - Define three columns: 'StudentName', 'Score', 'Subject'
        - Store it in self.data attribute
        
        Example:
            tracker = StudentTracker()
            # tracker.data should be an empty DataFrame with 0 rows
            # but 3 columns: StudentName, Score, Subject
        
        Hint: Use pd.DataFrame(columns=[...]) to create an empty DataFrame
        """
        """ YOUR CODE HERE """

    def record_grade(self, name: str, score: float, subject: str) -> None:
        """
        Add a new student performance record to the DataFrame.
        
        Parameters:
            name (str): Student's name
            score (float): Score obtained (e.g., 85.0, 90.5)
            subject (str): Subject name (e.g., 'Math', 'Science')
        
        Returns:
            None (This method modifies self.data in place)
        
        Implementation Guide:
        1. Create a new row/record with the provided values
        2. Add it to self.data
        3. Reset index to maintain consistency
        
        Step-by-step:
        a) Create a temporary DataFrame with one row:
           - Column 'StudentName': [name]
           - Column 'Score': [score]
           - Column 'Subject': [subject]
        
        b) Use pd.concat() to append to self.data:
           - Combine self.data with the new record
           - Use ignore_index=True to reset the index
        
        Example:
            tracker.record_grade("Alice", 85, "Math")
            tracker.record_grade("Bob", 90, "Science")
            # After 2 calls, tracker.data should have 2 rows
        
        Common Mistakes:
        - Using df.append() (deprecated in newer pandas)
        - Not using ignore_index=True
        - Forgetting to reassign: self.data = pd.concat(...)
        
        Hint: Use pd.concat([self.data, new_record], ignore_index=True)
        """
        new_record = pd.DataFrame({
            'StudentName': [name],
            'Score': [score],
            'Subject': [subject]
        })
        """ YOUR CODE HERE """

    def get_subject_avg(self, subject: str) -> float:
        """
        Calculate the average score for a specific subject.
        
        Parameters:
            subject (str): Subject name to filter by
        
        Returns:
            float: Average score for the subject
                   Returns 0.0 if subject is not found
        
        Implementation Guide:
        1. Filter the DataFrame for rows matching the subject
        2. Calculate the mean of the 'Score' column
        3. Handle the case when subject doesn't exist
        
        Step-by-step:
        a) Filter self.data where 'Subject' column equals the input subject:
           filtered_data = self.data[self.data['Subject'] == subject]
        
        b) Check if the filtered data is empty:
           - If empty (no records for this subject): return 0.0
           - If not empty: calculate the mean score
        
        c) Calculate mean using: filtered_data['Score'].mean()
        
        Example:
            tracker.record_grade("Alice", 85, "Math")
            tracker.record_grade("Bob", 85, "Math")
            result = tracker.get_subject_avg("Math")
            # result should be 85.0 (average of 85 and 85)
            
            result = tracker.get_subject_avg("Physics")
            # result should be 0.0 (no records for Physics)
        
        Hint: Use Boolean indexing with [] to filter:
              self.data[self.data['Subject'] == subject]
        """
        """ YOUR CODE HERE """

    def get_top_scorers(self, threshold: float) -> list:
        """
        Get list of unique student names with scores above threshold.
        
        Parameters:
            threshold (float): Minimum score to qualify
                             Students with Score > threshold are returned
        
        Returns:
            list: Unique student names with scores GREATER than threshold
                  Empty list if no students qualify
        
        Important: Use GREATER THAN (>), NOT greater than or equal (>=)
        
        Implementation Guide:
        1. Filter records where Score > threshold
        2. Get unique student names from filtered records
        3. Convert to a Python list
        
        Step-by-step:
        a) Filter self.data where 'Score' > threshold:
           Use Boolean indexing: self.data[self.data['Score'] > threshold]
        
        b) Extract unique student names:
           Use .unique() on 'StudentName' column
           This removes duplicates if a student has multiple records
        
        c) Convert to list:
           Use list() to convert numpy array to Python list
        
        Example:
            tracker.record_grade("Alice", 88, "Math")
            tracker.record_grade("Bob", 82, "Science")
            tracker.record_grade("Charlie", 70, "English")
            
            result = tracker.get_top_scorers(80)
            # result should be ['Alice', 'Bob'] (scores > 80)
            # Charlie's 70 is NOT included (70 is not > 80)
        
        Common Mistakes:
        - Using >= instead of > (the problem requires >)
        - Not using .unique() (might return duplicates)
        - Forgetting to convert to list
        
        Hint: self.data[self.data['Score'] > threshold]['StudentName'].unique()
        """
        """ YOUR CODE HERE """

    def get_summary_stats(self) -> dict:
        """
        Get summary statistics about the records.
        
        Returns:
            dict: Dictionary with two keys:
                  - 'total_records': Total number of records (rows) in self.data
                  - 'unique_students': Count of unique student names
        
        Implementation Guide:
        1. Count total rows in self.data
        2. Count unique values in 'StudentName' column
        3. Return as a dictionary with exact keys
        
        Step-by-step:
        a) Get total records:
           Use len(self.data) to count rows
        
        b) Get unique students:
           Use self.data['StudentName'].nunique() 
           (nunique = number of unique values)
        
        c) Return as dictionary:
           return {
               'total_records': total_count,
               'unique_students': unique_count
           }
        
        Example:
            tracker.record_grade("Alice", 85, "Math")
            tracker.record_grade("Alice", 90, "Science")  # Alice again
            tracker.record_grade("Bob", 78, "Math")
            tracker.record_grade("Charlie", 88, "English")
            
            result = tracker.get_summary_stats()
            # result should be:
            # {
            #     'total_records': 4,    (4 individual records)
            #     'unique_students': 3   (Alice, Bob, Charlie)
            # }
        
        Important Keys:
        - Keys must be exactly: 'total_records' and 'unique_students'
        - Case-sensitive! Not 'Total_Records' or 'unique_Students'
        
        Hint: len() for total rows, .nunique() for unique count
        """
        """ YOUR CODE HERE """
