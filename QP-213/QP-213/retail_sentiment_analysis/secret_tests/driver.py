import importlib.util
import os
import sys
import pandas as pd
import random

def validate_method_exists(obj, method_name):
    """Check if method exists and is callable."""
    if not hasattr(obj, method_name):
        return False, f"Method '{method_name}' not found. Please check implementation."
    if not callable(getattr(obj, method_name)):
        return False, f"'{method_name}' is not callable. Make sure it's a method."
    return True, None

def test_student_code(solution_path):
    report_dir = os.path.dirname(solution_path)
    report_path = os.path.join(report_dir, "report.txt")
    
    # Load Student Solution
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(solution)
    except Exception as e:
        msg = f"IMPORT ERROR: {e}"
        print(msg)
        with open(report_path, "w", encoding="utf-8") as f: f.write(msg + "\n")
        return

    print("Running Tests for: Retail Sentiment Analysis (Professional Driver)\n")
    report_lines = ["Running Tests for: Retail Sentiment Analysis (Professional Driver)\n"]

    if not hasattr(solution, "SalesTracker"):
        msg = "ERROR: SalesTracker class not found in solution.py"
        print(msg); report_lines.append(msg)
        with open(report_path, "w", encoding="utf-8") as f: f.write("\n".join(report_lines) + "\n")
        return

    # Data Paths
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    sales_p = os.path.join(data_dir, "product_sales.csv")
    reviews_p = os.path.join(data_dir, "customer_reviews.csv")
    
    # Pre-load data for setup functions
    try:
        raw_sales = pd.read_csv(sales_p)
        raw_reviews = pd.read_csv(reviews_p)
    except Exception as e:
        print(f"CRITICAL ERROR: Data files missing. {e}"); return

    # Helper for Rounded Equality (Hardcoding Prevention Check)
    def compare_rounded(r, e, precision=1):
        try:
            if isinstance(r, (float, int)): return round(float(r), precision) == round(float(e), precision)
            if isinstance(r, dict):
                return all(compare_rounded(r[k], e.get(k)) for k in e)
            if isinstance(r, list):
                return all(compare_rounded(x, y) for x, y in zip(r, e))
            return str(r) == str(e)
        except: return False

    test_cases = [
        {
            "desc": "Initialize and Load DataFrames",
            "func": "load_csvs",
            "setup": lambda: solution.SalesTracker(),
            "call": lambda obj: (obj.load_csvs(sales_p, reviews_p), isinstance(obj.df_sales, pd.DataFrame)),
            "check": lambda res: res[1] == True,
            "expected_output": "SalesTracker.df_sales should be a pandas DataFrame.",
            "marks": 0
        },
        {
            "desc": "Filter sales by volume threshold",
            "func": "get_top_sellers",
            "setup": lambda: _setup_with_data(solution.SalesTracker(), raw_sales),
            "call": lambda obj: len(obj.get_top_sellers(100)),
            "check": lambda res: res == len(raw_sales[raw_sales['Units_Sold'] >= 100]),
            "expected_output": f"Expected {len(raw_sales[raw_sales['Units_Sold'] >= 100])} rows for threshold 100.",
            "marks": 3
        },
        {
            "desc": "Categorical price analysis (Mean)",
            "func": "category_price_analysis",
            "setup": lambda: _setup_with_data(solution.SalesTracker(), raw_sales),
            "call": lambda obj: obj.category_price_analysis().to_dict(),
            "check": lambda res: compare_rounded(res, raw_sales.groupby('Category')['Unit_Price'].mean().to_dict()),
            "expected_output": "Dictionary of categories and mean prices.",
            "marks": 3
        },
        {
            "desc": "Product-level review aggregation",
            "func": "aggregate_reviews",
            "setup": lambda: solution.SentimentAnalyzer(),
            "call": lambda obj: obj.aggregate_reviews(raw_reviews).to_dict(orient='records'),
            "check": lambda res: compare_rounded(res, raw_reviews.groupby('Product_ID')['Rating'].mean().reset_index().to_dict(orient='records')),
            "expected_output": "Aggregated ratings per Product_ID.",
            "marks": 3
        },
        {
            "desc": "Cross-dataset merging logic",
            "func": "get_correlation_summary",
            "setup": lambda: solution.SentimentAnalyzer(),
            "call": lambda obj: len(obj.get_correlation_summary(raw_sales, raw_reviews)),
            "check": lambda res: res == len(pd.merge(raw_sales[['Product_ID', 'Units_Sold']], raw_reviews.groupby('Product_ID')['Rating'].mean().reset_index(), on='Product_ID', how='inner')),
            "expected_output": "Total rows in merged DataFrame matches reference join.",
            "marks": 3
        },
        {
            "desc": "Discount performance analysis",
            "func": "discount_performance",
            "setup": lambda: solution.SentimentAnalyzer(),
            "call": lambda obj: obj.discount_performance(raw_sales),
            "check": lambda res: compare_rounded(res, _ref_discount(raw_sales)),
            "expected_output": "Avg sales for Discounted vs FullPrice items.",
            "marks": 4
        },
        {
            "desc": "Sales opportunity detection logic",
            "func": "detect_opportunities",
            "setup": lambda: solution.SentimentAnalyzer(),
            "call": lambda obj: sorted(obj.detect_opportunities(_ref_merge(raw_sales, raw_reviews))),
            "check": lambda res: res == _ref_opps(raw_sales, raw_reviews),
            "expected_output": "List of high-rating, low-sales Product_IDs.",
            "marks": 4
        }
    ]

    total_score = 0
    for idx, case in enumerate(test_cases, 1):
        marks = case["marks"]
        try:
            # Setup Object
            obj = case["setup"]()
            
            # Verify Method
            valid, err = validate_method_exists(obj, case["func"])
            if not valid:
                msg = f"FAIL TC{idx} [{case['desc']}]: {err}"
                print(msg); report_lines.append(msg); continue

            # Execute & Check
            result = case["call"](obj)
            passed = case["check"](result)

            if passed:
                total_score += marks
                msg = f"PASS TC{idx} [{case['desc']}] ({marks}/{marks})"
            else:
                msg = f"FAIL TC{idx} [{case['desc']}] (0/{marks})\n  Expected: {case['expected_output']}\n  Got: {repr(result)}"
        except Exception as e:
            msg = f"FAIL TC{idx} [{case['desc']}] (0/{marks}) | Error: {type(e).__name__}: {e}"
        print(msg); report_lines.append(msg)

    score_line = f"\nSCORE: {total_score}/20.0"
    print(score_line); report_lines.append(score_line)
    with open(report_path, "w", encoding="utf-8") as f: f.write("\n".join(report_lines) + "\n")

# Helper Functions for Data Injection / Reference Logic
def _setup_with_data(obj, df):
    obj.df_sales = df.copy()
    return obj

def _ref_discount(df):
    d = df[df['Discount_Applied'] == True]['Units_Sold'].mean()
    f = df[df['Discount_Applied'] == False]['Units_Sold'].mean()
    return {'Discounted_Avg_Sales': round(float(d), 2), 'FullPrice_Avg_Sales': round(float(f), 2)}

def _ref_merge(df_s, df_r):
    agg = df_r.groupby('Product_ID')['Rating'].mean().reset_index()
    return pd.merge(df_s[['Product_ID', 'Units_Sold']], agg, on='Product_ID', how='inner')

def _ref_opps(df_s, df_r):
    df_m = _ref_merge(df_s, df_r)
    m = df_m['Units_Sold'].median()
    opps = df_m[(df_m['Rating'] > 4.0) & (df_m['Units_Sold'] < m)]
    return sorted(opps['Product_ID'].unique().tolist())

if __name__ == "__main__":
    sol_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(sol_file)
