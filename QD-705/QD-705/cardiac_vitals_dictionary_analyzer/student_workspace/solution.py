class HealthMonitor:
    """Health Monitoring System using Python Dictionaries."""
    
    def __init__(self):
        """Initialize with default records."""
        # TODO: Initialize self.records with default records dict
        pass
    
    def clean_records(self) -> None:
        """Drop all rows where 'HeartRate' is None and print removed count."""
        pass
    
    def find_highest_rate(self) -> None:
        """Find the maximum heart rate and print it."""
        pass
    
    def patient_averages(self) -> None:
        """Calculate and print average heart rate per patient sorted alphabetically."""
        pass
    
    def high_risk(self, threshold: int) -> None:
        """Identify and print sorted list of unique PatientIDs above threshold."""
        pass
    
    def count_high_risk(self, threshold: int) -> None:
        """Count and print unique high-risk patients meeting threshold."""
        pass
