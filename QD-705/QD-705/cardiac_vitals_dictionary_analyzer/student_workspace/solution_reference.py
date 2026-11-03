class HealthMonitor:
    """
    Health Monitoring System using Python Dictionaries.
    Manages patient health data with dict operations.
    """
    
    def __init__(self):
        """Initialize with default records."""
        self.records = {
            0: {'PatientID': 'P01', 'Day': 'Mon', 'HeartRate': 72},
            1: {'PatientID': 'P02', 'Day': 'Mon', 'HeartRate': None},
            2: {'PatientID': 'P01', 'Day': 'Tue', 'HeartRate': 75},
            3: {'PatientID': 'P03', 'Day': 'Mon', 'HeartRate': 105},
            4: {'PatientID': 'P04', 'Day': 'Tue', 'HeartRate': 68},
            5: {'PatientID': 'P05', 'Day': 'Mon', 'HeartRate': 80},
            6: {'PatientID': 'P06', 'Day': 'Mon', 'HeartRate': None},
            7: {'PatientID': 'P01', 'Day': 'Wed', 'HeartRate': 70},
            8: {'PatientID': 'P03', 'Day': 'Tue', 'HeartRate': 110},
            9: {'PatientID': 'P04', 'Day': 'Wed', 'HeartRate': 75},
            10: {'PatientID': 'P02', 'Day': 'Tue', 'HeartRate': 85},
            11: {'PatientID': 'P05', 'Day': 'Wed', 'HeartRate': 90}
        }
    
    def clean_records(self) -> None:
        """Drop all rows where 'HeartRate' is None and print removed count."""
        if self.records is None:
            print("Removed Records: 0")
            return
        initial_count = len(self.records)
        self.records = {k: v for k, v in self.records.items() if v['HeartRate'] is not None}
        print(f"Removed Records: {initial_count - len(self.records)}")
    
    def find_highest_rate(self) -> None:
        """Find the maximum heart rate and print it."""
        if self.records is None or not self.records:
            print("Highest Heart Rate: 0")
            return
        rates = [v['HeartRate'] for v in self.records.values() if v['HeartRate'] is not None]
        if rates:
            print(f"Highest Heart Rate: {max(rates)}")
        else:
            print("No heart rate records found")
    
    def patient_averages(self) -> None:
        """Calculate and print average heart rate per patient sorted alphabetically."""
        if self.records is None or not self.records:
            return
        groups = {}
        for v in self.records.values():
            if v['HeartRate'] is not None:
                pid = v['PatientID']
                groups.setdefault(pid, []).append(v['HeartRate'])
        
        for pid in sorted(groups.keys()):
            rates = groups[pid]
            average = round(sum(rates) / len(rates), 2)
            print(f"{pid}: {average:.2f}")
    
    def high_risk(self, threshold: int) -> None:
        """Identify and print sorted list of unique PatientIDs above threshold."""
        if self.records is None or not self.records:
            print("High Risk Patients:")
            return
        high_risk_pts = set()
        for v in self.records.values():
            if v['HeartRate'] is not None and v['HeartRate'] > threshold:
                high_risk_pts.add(v['PatientID'])
        print(f"High Risk Patients: {', '.join(sorted(list(high_risk_pts)))}")
    
    def count_high_risk(self, threshold: int) -> None:
        """Count and print unique high-risk patients meeting threshold."""
        if self.records is None or not self.records:
            print("High Risk Patient Count: 0")
            return
        high_risk_pts = set()
        for v in self.records.values():
            if v['HeartRate'] is not None and v['HeartRate'] > threshold:
                high_risk_pts.add(v['PatientID'])
        print(f"High Risk Patient Count: {len(high_risk_pts)}")
