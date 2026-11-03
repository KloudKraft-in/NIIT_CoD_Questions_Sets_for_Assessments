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
    report_dir = os.path.join(os.path.dirname(__file__), "..", "reports")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    print("🧪 Running Tests for: Student Exam Performance Analyzer\n")
    report_lines = ["🧪 Running Tests for: Student Exam Performance Analyzer\n"]

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

    log4j_path = Path(__file__).resolve().parent.parent / "student_workspace" / "log4j.properties"
    if not log4j_path.exists():
        msg = f"❌ ERROR: log4j.properties not found at:\n   {log4j_path}"
        print(msg)
        report_lines.append(msg)
        return

    log4j_clean = str(log4j_path).replace("\\", "/")
    log4j_url = f"file:///{quote(log4j_clean)}"
    print(f"✔️ Using log4j.properties from:\n   {log4j_clean}\n")
    report_lines.append(f"✔️ Using log4j.properties from:\n   {log4j_clean}\n")
    print("▶️ Initializing SparkSession…")

    try:
        stdout, stderr = sys.stdout, sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        spark = (
            SparkSession.builder
            .appName("StudentExamPerformance")
            .master("local[*]")
            .config("spark.hadoop.home.dir", HADOOP_HOME)
            .config("spark.driver.extraJavaOptions", f'-Dlog4j.configuration={log4j_url}')
            .config("spark.executor.extraJavaOptions", f'-Dlog4j.configuration={log4j_url}')
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
        return

    # Load solution
    try:
        spec = importlib.util.spec_from_file_location("student_solution", solution_path)
        student_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(student_module)
        analyzer = student_module.ExamAnalyzer(spark)
    except Exception as e:
        msg = f"❌ Failed to load solution.py: {e}"
        print(msg)
        report_lines.append(msg)
        spark.stop()
        return

    # Paths
    students_path = Path(__file__).resolve().parent.parent / "data" / "students.csv"
    scores_path = Path(__file__).resolve().parent.parent / "data" / "scores.csv"

    if not students_path.exists() or not scores_path.exists():
        msg = f"❌ Missing CSV files:\n   students.csv: {students_path.exists()} | scores.csv: {scores_path.exists()}"
        print(msg)
        report_lines.append(msg)
        spark.stop()
        return

    # Fallback DataFrames for all tests
    fallback_students = spark.read.csv(str(students_path), header=True, inferSchema=True)
    fallback_scores = spark.read.csv(str(scores_path), header=True, inferSchema=True)
    joined_df = fallback_students.join(fallback_scores, "student_id", "inner")

    test_cases = [
        {
            "desc": "Load student and score data",
            "func": "load_data",
            "input": (str(students_path), str(scores_path)),
            "expected_type": tuple,
            "marks": 3
        },
        {
            "desc": "Join student and score data",
            "func": "join_data",
            "input": (fallback_students, fallback_scores),
            "expected_type": DataFrame,
            "marks": 3
        },
        {
            "desc": "Find top scorer per subject",
            "func": "top_scorer_per_subject",
            "input": (joined_df,),
            "expected_type": DataFrame,
            "marks": 4
        },
        {
            "desc": "Average score per class",
            "func": "average_score_by_class",
            "input": (joined_df,),
            "expected_type": DataFrame,
            "marks": 3
        },
        {
            "desc": "Students who missed all exams",
            "func": "students_missed_all_exams",
            "input": (fallback_students, fallback_scores),
            "expected_type": list,
            "marks": 3
        },
        {
            "desc": "Student with highest average score",
            "func": "top_average_scorer",
            "input": (joined_df,),
            "expected_type": int,
            "marks": 4
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

            if 'pass' in src and len(src) < 80:
                msg = f"❌ Visible Test Case {idx} Failed: {case['desc']} | Reason: Contains only 'pass'"
                print(msg)
                report_lines.append(msg)
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
