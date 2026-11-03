import os
import importlib.util
from pathlib import Path
from pyspark.sql import SparkSession, DataFrame
import contextlib
from io import StringIO
import datetime
import sys
import inspect
from urllib.parse import quote

def test_student_code(solution_path):
    # Set up report file
    report_dir = os.path.join(os.path.dirname(__file__), "..", "reports")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    print("🧪 Running Tests for: Retail Sales Analysis\n")
    report_lines = ["🧪 Running Tests for: Retail Sales Analysis\n"]

    # Set environment variables
    JAVA_HOME = r"C:\Program Files\Java\jdk-17"
    HADOOP_HOME = r"C:\hadoop"
    os.environ["JAVA_HOME"] = JAVA_HOME
    os.environ["HADOOP_HOME"] = HADOOP_HOME
    os.environ["PATH"] = (
        os.path.join(JAVA_HOME, "bin") + ";" +
        os.path.join(HADOOP_HOME, "bin") + ";" +
        os.environ.get("PATH", "")
    )
    os.environ["SPARK_SUBMIT_OPTS"] = (
        "-Dspark.ui.showConsoleProgress=false "
        "-Dorg.apache.spark.internal.Logging.noConsoleLog=true"
    )

    # Prepare log4j.properties
    log4j_path = Path(__file__).resolve().parent.parent / "student_workspace" / "log4j.properties"
    if not log4j_path.exists():
        msg = f"❌ ERROR: log4j.properties not found at:\n   {log4j_path}"
        print(msg)
        report_lines.append(msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write("\n".join(report_lines) + "\n")
        return

    log4j_path_clean = str(log4j_path).replace("\\", "/")
    log4j_url = f"file:///{quote(log4j_path_clean)}"
    print(f"✔️ Using log4j.properties from:\n   {log4j_path_clean}\n")
    report_lines.append(f"✔️ Using log4j.properties from:\n   {log4j_path_clean}\n")
    print("▶️ Initializing SparkSession…")

    # Start SparkSession
    try:
        stdout, stderr = sys.stdout, sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()

        spark = (
            SparkSession.builder
            .appName("RetailSalesAnalysis")
            .master("local[*]")
            .config("spark.hadoop.home.dir", HADOOP_HOME)
            .config("spark.driver.extraJavaOptions", f'-Dlog4j.configuration={log4j_url}')
            .config("spark.executor.extraJavaOptions", f'-Dlog4j.configuration={log4j_url}')
            .config("spark.ui.showConsoleProgress", "false")
            .getOrCreate()
        )
        spark.sparkContext.setLogLevel("OFF")
        sys.stdout = stdout
        sys.stderr = stderr

        report_lines.append("✔️ SparkSession created!\n")
    except Exception as e:
        sys.stdout = stdout
        sys.stderr = stderr
        msg = f"❌ Failed to start SparkSession: {e}"
        print(msg)
        report_lines.append(msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write("\n".join(report_lines) + "\n")
        return

    # Load student solution
    try:
        spec = importlib.util.spec_from_file_location("student_solution", solution_path)
        student_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(student_module)
        analyzer = student_module.RetailSalesAnalyzer(spark)
    except Exception as e:
        msg = f"❌ Failed to load solution.py: {e}"
        print(msg)
        report_lines.append(msg)
        spark.stop()
        with open(report_path, "a", encoding="utf-8") as f:
            f.write("\n".join(report_lines) + "\n")
        return

    # Load input data CSV
    sales_path = Path(__file__).resolve().parent.parent / "data" / "sales.csv"
    if not sales_path.exists():
        msg = f"❌ Missing CSV file:\n   sales.csv exists: {sales_path.exists()}"
        print(msg)
        report_lines.append(msg)
        spark.stop()
        with open(report_path, "a", encoding="utf-8") as f:
            f.write("\n".join(report_lines) + "\n")
        return

    # Define test cases
    test_cases = [
        {
            "desc": "Load transaction data",
            "func": "load_transactions",
            "input": (str(sales_path),),
            "expected_type": DataFrame,
            "marks": 5
        },
        {
            "desc": "Total purchase value",
            "func": "total_purchase_value",
            "input": (spark.read.csv(str(sales_path), header=True, inferSchema=True),),
            "expected_type": float,
            "marks": 5
        },
        {
            "desc": "Top product category",
            "func": "top_product_category",
            "input": (spark.read.csv(str(sales_path), header=True, inferSchema=True),),
            "expected_type": tuple,
            "marks": 5
        },
        {
            "desc": "Top 3 products by quantity",
            "func": "top_n_products",
            "input": (spark.read.csv(str(sales_path), header=True, inferSchema=True),),
            "expected_type": list,
            "marks": 5
        }
    ]

    total_score = 0
    max_score = 0

    print(f"=== Test Run at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
    report_lines.append(f"=== Test Run at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")

    for idx, case in enumerate(test_cases, 1):
        marks = case["marks"]
        max_score += marks

        try:
            func = getattr(analyzer, case["func"])
            src = inspect.getsource(func).replace(" ", "").replace("\n", "").lower()

            if "pass" in src and len(src) < 80:
                msg = f"❌ Visible Test Case {idx} Failed: {case['desc']} | Reason: Contains only 'pass'"
                report_lines.append(msg)
                print(msg)
                continue

            result = func(*case["input"])
            passed = isinstance(result, case["expected_type"])

            if passed:
                total_score += marks
                msg = f"✅ Visible Test Case {idx} Passed: {case['desc']}"
            else:
                msg = f"❌ Visible Test Case {idx} Failed: {case['desc']} | Reason: Output mismatch"

        except Exception as e:
            msg = f"❌ Visible Test Case {idx} Crashed: {case['desc']} | Error: {str(e)}"

        print(msg)
        report_lines.append(msg)

    print("\n✔️ Tests complete, stopping Spark…")
    report_lines.append("\n✔️ Tests complete, stopping Spark…")
    spark.stop()
    print("✔️ Done!")
    report_lines.append("✔️ Done!")

    score_line = f"\n🎯 TOTAL SCORE: {total_score}/{max_score}\n"
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")


if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
