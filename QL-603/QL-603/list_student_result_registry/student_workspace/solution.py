class ResultRegistry:
    """Manage student scores and provide analysis operations."""

    def __init__(self):
        """Initialize the score list with sample data."""
        self.scores = [45, 78, 92, 55, 88, 67, 95, 52]

    def create_status_dict(self) -> dict:
        """Map each score to its pass/fail status."""
        # Hint: Iterate through self.scores and create a dictionary mapping each score 
        # to "Pass" if >= 80, otherwise "Fail".
        
        """ YOUR CODE HERE """
        pass

    def find_highest_score(self) -> int:
        """Find and return the highest score."""
        # Hint: Use the built-in max() function on self.scores.

        """ YOUR CODE HERE """
        pass

    def calculate_average(self) -> float:
        """Calculate and return the average score rounded to 1 decimal place."""
        # Hint: Calculate the sum divided by the length, and use round(result, 1).

        """ YOUR CODE HERE """
        pass

    def get_passing_scores(self) -> list:
        """Get all passing scores (>= 80) sorted in descending order."""
        # Hint: Use a list comprehension to filter scores >= 80, then sort with reverse=True.

        """ YOUR CODE HERE """
        pass

    def get_failed_scores(self) -> list:
        """Get all failed scores (< 80) sorted in ascending order."""
        # Hint: Use a list comprehension to filter scores < 80, then use the sort method.

        """ YOUR CODE HERE """
        pass

    def count_pass_fail(self) -> dict:
        """Count the total number of passing and failing students."""
        # Hint: Use create_status_dict() to get all statuses, then count the occurrences 
        # of "Pass" and "Fail".
        pass
