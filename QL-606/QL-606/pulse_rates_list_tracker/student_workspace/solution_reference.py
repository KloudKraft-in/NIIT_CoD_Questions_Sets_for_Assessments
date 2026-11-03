class HealthMonitor:
    """
    Health Monitoring System using Python Lists.
    Manages patient health data with list operations.
    """
    
    def __init__(self):
        """Initialize with default records."""
        self.records = [
            ['P01', 'Mon', 72],
            ['P02', 'Mon', None],
            ['P01', 'Tue', 75],
            ['P03', 'Mon', 105],
            ['P04', 'Tue', 68],
            ['P05', 'Mon', 80],
            ['P06', 'Mon', None],
            ['P01', 'Wed', 70],
            ['P03', 'Tue', 110],
            ['P04', 'Wed', 75],
            ['P02', 'Tue', 85],
            ['P05', 'Wed', 90]
        ]
    
    def clean_records(self) -> int:
        """Drop all rows where the HeartRate is None."""
        if self.records is None:
            return 0
        initial_count = len(self.records)
        self.records = [r for r in self.records if r[2] is not None]
        return initial_count - len(self.records)
    
    def find_highest_rate(self) -> int:
        """Find the maximum heart rate value across all cleaned records."""
        if self.records is None or not self.records:
            return 0
        rates = [r[2] for r in self.records if r[2] is not None]
        return max(rates) if rates else 0
    
    def patient_averages(self) -> dict:
        """Calculate the mean HeartRate for each unique PatientID in the records."""
        if self.records is None or not self.records:
            return {}
        groups = {}
        for r in self.records:
            if r[2] is not None:
                pid = r[0]
                groups.setdefault(pid, []).append(r[2])
        
        averages = {}
        for pid, rates in groups.items():
            averages[pid] = round(sum(rates) / len(rates), 2)
        return averages
    
    def high_risk(self, threshold: int) -> list:
        """Identify unique PatientID values who have at least one reading strictly greater than the threshold."""
        if self.records is None or not self.records:
            return []
        high_risk_pts = set()
        for r in self.records:
            if r[2] is not None and r[2] > threshold:
                high_risk_pts.add(r[0])
        return sorted(list(high_risk_pts))
    
    def count_high_risk(self, threshold: int) -> int:
        """Count the number of unique high-risk patients meeting the threshold criteria."""
        return len(self.high_risk(threshold))
