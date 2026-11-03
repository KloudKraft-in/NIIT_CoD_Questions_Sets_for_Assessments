class ScoreManager:
    """Manage student scores and provide analysis operations."""

    def __init__(self):
        """Initialize the score list with sample data."""
        self.scores = [45, 78, 92, 55, 88, 67, 95, 52]

    def create_status_dict(self) -> dict:
        """
        Create a dictionary mapping each score to its pass/fail status.
        
        Returns:
            Dictionary with scores as keys and pass/fail status as values
            Pass threshold: score >= 80
        """
        """Your code here"""
        return status_dict

    def find_highest_score(self) -> int:
        """
        Find and return the highest score.
        
        Returns:
            Maximum score from the list
        """
        """Your code here"""

    def calculate_average(self) -> float:
        """
        Calculate and return the average score.
        
        Returns:
            Average score rounded to 1 decimal place
        """
        """Your code here"""
        return round(average, 1)

    def get_passing_scores(self) -> list:
        """
        Get all passing scores sorted in descending order.
        
        Returns:
            List of scores >= 80 sorted in descending order
        """
        """Your code here"""
        return sorted(passing, reverse=True)
