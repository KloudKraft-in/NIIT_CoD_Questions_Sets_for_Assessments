import os
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
import sys
import pandas as pd
from datetime import datetime

# Add current directory to sys.path to import solution.py
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def run_tests():
    print("-" * 50)
    print("TESTING SOLUTION: solution.py")
    print("-" * 50)
    
    try:
        from solution import Warehouse, SupplyOptimizer
    except ImportError as e:
        print(f"Error: Could not import classes from solution.py. {e}")
        return

    results = []
    total_marks = 0

    # Paths to data
    sales_csv = os.path.join(current_dir, "..", "data", "sales_velocity.csv")

    # TC1: Initialization
    try:
        so_tc1 = SupplyOptimizer()
        if hasattr(so_tc1, 'df_stock') and so_tc1.df_stock is None:
            results.append(("TC1", "Initialization", "Passed", 0))
        else:
            results.append(("TC1", "Initialization", "Failed (Incorrect attributes)", 0))
    except Exception as e:
        results.append(("TC1", "Initialization", f"Failed ({e})", 0))

    # TC2: Load Data
    try:
        so_tc2 = SupplyOptimizer()
        # Robustness: Force inject if __init__ is missing it
        if not hasattr(so_tc2, 'df_stock'): so_tc2.df_stock = None
        if not hasattr(so_tc2, 'df_sales'): so_tc2.df_sales = None
        
        # Create temporary dummy CSVs to test load_data
        dummy_stock = "sku,warehouse_id,stock\nA1,W1,10\n"
        dummy_sales = "sku,daily_avg_sales\nA1,2\n"
        with open("test_stock.csv", "w") as f: f.write(dummy_stock)
        with open("test_sales.csv", "w") as f: f.write(dummy_sales)
        
        so_tc2.load_data("test_stock.csv", "test_sales.csv")
        os.remove("test_stock.csv")
        os.remove("test_sales.csv")
        
        if so_tc2.df_stock is not None and len(so_tc2.df_stock) == 1:
            results.append(("TC2", "Data Loading", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC2", "Data Loading", "Failed (DFs not loaded)", 0))
    except Exception as e:
        results.append(("TC2", "Data Loading", f"Failed ({e})", 0))

    # TC3: Inner Join (Independent)
    try:
        so_tc3 = SupplyOptimizer()
        # Direct Injection: Forcefully set/overwrite the DataFrames
        so_tc3.df_stock = pd.DataFrame({'SKU': ['A', 'B'], 'Stock': [10, 20]})
        so_tc3.df_sales = pd.DataFrame({'SKU': ['A', 'C'], 'Daily_Avg_Sales': [2, 5]})
        
        merged = so_tc3.get_merged_data()
        if merged is not None and len(merged) == 1 and list(merged['SKU']) == ['A']:
            results.append(("TC3", "Data Integration", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC3", "Data Integration", f"Failed (Rows: {len(merged) if merged is not None else 0})", 0))
    except Exception as e:
        results.append(("TC3", "Data Integration", f"Failed ({e})", 0))

    # TC4: Median Imputation (Independent)
    try:
        so_tc4 = SupplyOptimizer()
        # Direct Injection
        so_tc4.df_sales = pd.DataFrame({'SKU': ['A', 'B', 'C'], 'Daily_Avg_Sales': [2, 10, None]})
        so_tc4.fill_velocity_gaps()
        # Median of 2 and 10 is 6.0
        val = so_tc4.df_sales.loc[so_tc4.df_sales['SKU'] == 'C', 'Daily_Avg_Sales'].iloc[0]
        if val == 6.0:
            results.append(("TC4", "Cleaning Logic", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC4", "Cleaning Logic", f"Failed (Got {val}, expected 6.0)", 0))
    except Exception as e:
        results.append(("TC4", "Cleaning Logic", f"Failed ({e})", 0))

    # TC5: Days To Empty Calculation (Independent)
    try:
        so_tc5 = SupplyOptimizer()
        # Robustness: Mock get_merged_data so TC5 doesn't depend on merging logic
        so_tc5.get_merged_data = lambda: pd.DataFrame({'SKU': ['A'], 'Stock': [10], 'Daily_Avg_Sales': [2]})
        
        res_df = so_tc5.add_days_to_empty()
        if res_df is not None and 'Days_To_Empty' in res_df.columns:
            val = res_df.loc[0, 'Days_To_Empty']
            if val == 5.0:
                results.append(("TC5", "Velocity Analysis", "Passed", 5))
                total_marks += 5
            else:
                results.append(("TC5", "Velocity Analysis", f"Failed (Got {val}, expected 5.0)", 0))
        else:
            results.append(("TC5", "Velocity Analysis", "Failed (Column 'Days_To_Empty' missing in return)", 0))
    except Exception as e:
        results.append(("TC5", "Velocity Analysis", f"Failed ({e})", 0))

    # TC6: Critical Stock Filter (Independent)
    try:
        so_tc6 = SupplyOptimizer()
        # Robustness: Mock add_days_to_empty so TC6 only tests the filtering logic
        mock_df = pd.DataFrame({'SKU': ['A', 'B'], 'Days_To_Empty': [2.0, 5.0]})
        so_tc6.add_days_to_empty = lambda: mock_df
        
        critical = so_tc6.get_critical_stock(3.0)
        if list(critical) == ['A']:
            results.append(("TC6", "Priority Alert", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC6", "Priority Alert", f"Failed (Got {critical})", 0))
    except Exception as e:
        results.append(("TC6", "Priority Alert", f"Failed ({e})", 0))


    # TC7: Total Value (Independent)
    try:
        so_tc7 = SupplyOptimizer()
        # Direct Injection
        so_tc7.df_stock = pd.DataFrame({'SKU': ['A', 'B'], 'Stock': [10, 5]})
        costs = {'A': 100, 'B': 50}
        val = so_tc7.calculate_total_value(costs)
        if val == 1250.0:
            results.append(("TC7", "Financial Impact", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC7", "Financial Impact", f"Failed (Got {val}, expected 1250.0)", 0))
    except Exception as e:
        results.append(("TC7", "Financial Impact", f"Failed ({e})", 0))


    # Display Results
    print(f"{'TC ID':<10} | {'Description':<25} | {'Status':<30} | {'Marks':<10}")
    print("-" * 85)
    for tcid, desc, status, marks in results:
        print(f"{tcid:<10} | {desc:<25} | {status:<30} | {marks:<10}")
    print("-" * 85)
    print(f"TOTAL MARKS: {total_marks} / 30")
    print("-" * 50)

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
        f.write(f"Inventory Optimizer Audit Report - {report_content['timestamp']}\n")
        f.write("=" * 40 + "\n")
        for res in report_content['results']:
            f.write(f"{res['tcid']}: {res['status']} ({res['marks']} marks)\n")
        f.write("=" * 40 + "\n")
        f.write(f"Final Score: {total_marks}/30\n")

if __name__ == "__main__":
    run_tests()
