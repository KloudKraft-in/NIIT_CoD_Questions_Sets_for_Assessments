import os
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
import sys
import pandas as pd
from datetime import datetime

# Add current directory to sys.path to import solution.py
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def run_tests():
    print("-" * 85)
    print("TESTING SOLUTION: solution.py")
    print("-" * 85)
    
    try:
        from solution import SensorReading, TrendAnalyzer
    except ImportError as e:
        print(f"Error: Could not import classes from solution.py. {e}")
        return

    results = []
    total_marks = 0

    # TC1: Initialization
    try:
        ta_tc1 = TrendAnalyzer()
        if hasattr(ta_tc1, 'df') and ta_tc1.df is None:
            results.append(("TC1", "Initialization", "Passed", 0))
        else:
            results.append(("TC1", "Initialization", "Failed (Incorrect attributes)", 0))
    except Exception as e:
        results.append(("TC1", "Initialization", f"Failed ({e})", 0))

    # TC2: Data Ingestion (Independent)
    try:
        ta_tc2 = TrendAnalyzer()
        # Create a small dummy CSV for testing ingestion
        test_csv = "Timestamp,Temperature,Sensor_ID\n2023-01-01 10:00:00,25.5,S1\n"
        with open("test_sensor.csv", "w") as f:
            f.write(test_csv)
            
        ta_tc2.load_data("test_sensor.csv")
        if os.path.exists("test_sensor.csv"): os.remove("test_sensor.csv")
        
        if ta_tc2.df is not None and len(ta_tc2.df) == 1:
            results.append(("TC2", "Data Ingestion", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC2", "Data Ingestion", "Failed (Data not loaded correctly)", 0))
    except Exception as e:
        results.append(("TC2", "Data Ingestion", f"Failed ({e})", 0))

    # TC3: Time-Series Conversion (Independent)
    try:
        ta_tc3 = TrendAnalyzer()
        # Robustness: Force inject a DataFrame with string timestamps
        ta_tc3.df = pd.DataFrame({
            'Timestamp': ['2023-01-01 08:00:00', '2023-01-01 12:00:00'],
            'Temperature': [20.0, 30.0]
        })
        ta_tc3.convert_to_datetime()
        if pd.api.types.is_datetime64_any_dtype(ta_tc3.df['Timestamp']):
            results.append(("TC3", "Format Conversion", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC3", "Format Conversion", "Failed (Column not converted)", 0))
    except Exception as e:
        results.append(("TC3", "Format Conversion", f"Failed ({e})", 0))

    # TC4: Working Hours Filter (Independent)
    try:
        ta_tc4 = TrendAnalyzer()
        # Robustness: Force inject datetime DataFrame
        ta_tc4.df = pd.DataFrame({
            'Timestamp': pd.to_datetime(['2023-01-01 08:00:00', '2023-01-01 10:00:00', '2023-01-01 18:00:00']),
            'Temperature': [10.0, 20.0, 30.0]
        })
        ta_tc4.filter_business_hours()
        # Should only keep 10:00:00 (row 1)
        if len(ta_tc4.df) == 1 and ta_tc4.df.iloc[0]['Timestamp'].hour == 10:
            results.append(("TC4", "Business Hours Logic", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC4", "Business Hours Logic", f"Failed (Rows: {len(ta_tc4.df)})", 0))
    except Exception as e:
        results.append(("TC4", "Business Hours Logic", f"Failed ({e})", 0))

    # TC5: Hourly Resampling (Independent)
    try:
        ta_tc5 = TrendAnalyzer()
        # Robustness: Force inject data
        ta_tc5.df = pd.DataFrame({
            'Timestamp': pd.to_datetime(['2023-01-01 10:00:00', '2023-01-01 10:30:00', '2023-01-01 11:00:00']),
            'Temperature': [20.0, 40.0, 30.0]
        })
        hourly = ta_tc5.calculate_hourly_means()
        # 10:00 and 10:30 should result in 10:00 Mean = 30.0
        # 11:00 should result in 11:00 Mean = 30.0
        if hourly is not None and not hourly.empty:
            val_10 = hourly.loc[pd.Timestamp('2023-01-01 10:00:00'), 'Temperature']
            if val_10 == 30.0:
                results.append(("TC5", "Aggregation Logic", "Passed", 5))
                total_marks += 5
            else:
                results.append(("TC5", "Aggregation Logic", f"Failed (10h Mean: {val_10})", 0))
        else:
            results.append(("TC5", "Aggregation Logic", "Failed (Empty results)", 0))
    except Exception as e:
        results.append(("TC5", "Aggregation Logic", f"Failed ({e})", 0))

    # TC6: Alert Count Detection (Independent)
    try:
        ta_tc6 = TrendAnalyzer()
        # Robustness: Force inject the resampled DataFrame directly
        ta_tc6.hourly_df = pd.DataFrame(
            {'Temperature': [70.0, 80.0, 90.0, 60.0]},
            index=pd.date_range('2023-01-01 09:00:00', periods=4, freq='1h')
        )
        alerts = ta_tc6.get_heat_alerts(75.0)
        if alerts == 2:
            results.append(("TC6", "Alert Detection", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC6", "Alert Detection", f"Failed (Got {alerts}, expected 2)", 0))
    except Exception as e:
        results.append(("TC6", "Alert Detection", f"Failed ({e})", 0))

    # TC7: Peak Reading ID (Independent)
    try:
        ta_tc7 = TrendAnalyzer()
        # Robustness: Force inject raw data
        ta_tc7.df = pd.DataFrame({
            'Temperature': [50.0, 100.0, 75.0],
            'Sensor_ID': ['S1', 'S2', 'S3']
        })
        peak_id = ta_tc7.get_max_reading_id()
        if peak_id == 'S2':
            results.append(("TC7", "Peak Lookup", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC7", "Peak Lookup", f"Failed (Got {peak_id})", 0))
    except Exception as e:
        results.append(("TC7", "Peak Lookup", f"Failed ({e})", 0))


    # Display Results
    print(f"{'TC ID':<10} | {'Description':<25} | {'Status':<30} | {'Marks':<10}")
    print("-" * 85)
    for tcid, desc, status, marks in results:
        print(f"{tcid:<10} | {desc:<25} | {status:<30} | {marks:<10}")
    print("-" * 85)
    print(f"TOTAL MARKS: {total_marks} / 30")
    print("-" * 85)

    # Generate Report
    report_content = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_marks": total_marks,
        "results": [
            {"tcid": r[0], "description": r[1], "status": r[2], "marks": r[3]} for r in results
        ]
    }
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = os.path.abspath(os.path.join(current_dir, "..", "reports"))
    os.makedirs(report_dir, exist_ok=True)
    report_filename = f"report_{timestamp}.txt"
    report_path = os.path.join(report_dir, report_filename)
    
    with open(report_path, "w") as f:
        f.write(f"IoT Sensor Trend Engine Report - {report_content['timestamp']}\n")
        f.write("=" * 40 + "\n")
        for res in report_content['results']:
            f.write(f"{res['tcid']}: {res['status']} ({res['marks']} marks)\n")
        f.write("=" * 40 + "\n")
        f.write(f"Final Score: {total_marks}/30\n")

if __name__ == "__main__":
    run_tests()
