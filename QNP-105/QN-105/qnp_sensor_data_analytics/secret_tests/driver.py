import os
import sys
import importlib.util
import numpy as np
import random
import matplotlib.pyplot as plt

# Use Agg backend for headless testing
import matplotlib
matplotlib.use('Agg')

class ReferenceDetector:
    def __init__(self, raw_readings: list):
        self.data = np.array(raw_readings, dtype=np.float64)

    def sanitize_data(self, min_bound: float, max_bound: float) -> list:
        self.data = np.clip(self.data, min_bound, max_bound)
        return self.data.tolist()

    def get_analysis_report(self) -> dict:
        return {
            "mean": float(np.mean(self.data)),
            "median": float(np.median(self.data)),
            "std": float(np.std(self.data))
        }

    def normalize_readings(self) -> list:
        d_min = np.min(self.data); d_max = np.max(self.data)
        if d_max == d_min: return [0.0] * len(self.data)
        return ((self.data - d_min) / (d_max - d_min)).tolist()

    def detect_extreme_outliers(self, threshold_std: float) -> list:
        mean, std = np.mean(self.data), np.std(self.data)
        if std == 0: return []
        z = np.abs((self.data - mean) / std)
        return np.where(z > threshold_std)[0].tolist()

    def calculate_moving_average(self, window_size: int) -> list:
        d = self.data.tolist()
        res = [sum(d[max(0, i-window_size+1):i+1])/len(d[max(0, i-window_size+1):i+1]) for i in range(len(d))]
        return res

    def compute_correlation(self, other_readings: list) -> float:
        other = np.array(other_readings, dtype=np.float64)
        if len(self.data) != len(other): return 0.0
        c = np.corrcoef(self.data, other)[0, 1]
        return float(c) if not np.isnan(c) else 0.0

    def generate_sensor_line_chart(self, title: str):
        fig, ax = plt.subplots()
        ax.plot(self.data); ax.set_title(title)
        return fig

    def generate_frequency_histogram(self, bins: int):
        fig, ax = plt.subplots()
        ax.hist(self.data, bins=bins)
        return fig

    def generate_correlation_scatter(self, other_readings: list):
        fig, ax = plt.subplots()
        ax.scatter(self.data, other_readings)
        return fig

def extract_plot_metadata(fig):
    """Extractions key plot data for hardcoding detection."""
    try:
        if not hasattr(fig, 'axes') or not fig.axes: return "EMPTY_FIG"
        ax = fig.axes[0]
        # Check for Lines (TC8)
        if ax.get_lines():
            return f"LINES:{ax.get_lines()[0].get_ydata().tolist()[:5]}"
        # Check for Collections (TC10 - Scatter)
        if ax.collections:
            return f"SCATTER:{ax.collections[0].get_offsets().tolist()[:5]}"
        # Check for Patches (TC9 - Histogram)
        if ax.patches:
            return f"HIST:{[p.get_height() for p in ax.patches[:5]]}"
        return "NO_DATA"
    except: return "ERROR"

def test_student_code(solution_path):
    report_dir = os.path.dirname(solution_path)
    report_path = os.path.join(report_dir, "report.txt")
    
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    try: spec.loader.exec_module(solution)
    except Exception as e:
        print(f"IMPORT ERROR: {e}"); return

    print("Running Tests for: Sensor Data Analytics (Independence & Unique Methods Mode)\n")
    report_lines = ["Running Tests for: Sensor Data Analytics (Independence & Unique Methods Mode)\n"]

    if not hasattr(solution, "SensorDataAnalytics"):
        print("ERROR: SensorDataAnalytics class not found"); return
    
    StudentClass = solution.SensorDataAnalytics
    ReferenceClass = ReferenceDetector
    
    tc_configs = [
        ("Verification of basic initialization", 0),
        ("Clip values to operational bounds", 2),
        ("Basic statistical report generation", 2),
        ("Linear Min-Max scaling of sensor data", 2),
        ("Standard Deviation based outlier check", 2),
        ("Rolling average smoothing (Windowing)", 2),
        ("Correlation with secondary sensor array", 2),
        ("Sensor data line chart visualization", 2),
        ("Frequency distribution histogram plot", 3),
        ("Cross-sensor correlation scatter plot", 3),
    ]

    random.seed(None)
    total_score = 0
    
    for i, (desc, marks) in enumerate(tc_configs, 1):
        try:
            def run_t(idx, cls_to_use, data_params):
                raw, p1, p2 = data_params
                obj = cls_to_use(raw)
                if idx == 1: return len(obj.data) if hasattr(obj, 'data') else "MISSING_ATTR"
                
                # State injection for TC2-TC10
                obj.data = np.array(raw, dtype=np.float64)
                
                if idx == 2: return obj.sanitize_data(p1, p2)
                if idx == 3: return obj.get_analysis_report()
                if idx == 4: return obj.normalize_readings()
                if idx == 5: return obj.detect_extreme_outliers(p1)
                if idx == 6: return obj.calculate_moving_average(int(p1))
                if idx == 7: return obj.compute_correlation(p2)
                if idx == 8: return obj.generate_sensor_line_chart(str(p1))
                if idx == 9: return obj.generate_frequency_histogram(int(float(p1)))
                if idx == 10: return obj.generate_correlation_scatter(p2)
                return None

            p_ok, h_det, none_ret = False, False, False
            
            # Dynamic Setup
            d_size = 10
            raw = [float(random.randint(20, 40)) for _ in range(d_size)]
            ext = [float(x * 1.5 + random.randint(1, 5)) for x in raw]
            if i == 2 or i == 5: raw[0] = 500.0
            params = (raw, 2.0, ext)
            
            if i >= 8:
                # Dual Run for Figures
                s_raw1 = [10.0, 20.0, 30.0]
                # Use type-consistent static params
                if i == 8: s_p1 = (s_raw1, "Static Title", s_raw1)
                elif i == 9: s_p1 = (s_raw1, 5, s_raw1)
                else: s_p1 = (s_raw1, s_raw1, s_raw1)
                
                res_s1 = run_t(i, StudentClass, s_p1)
                res_s2 = run_t(i, StudentClass, params)
                
                meta1 = extract_plot_metadata(res_s1)
                meta2 = extract_plot_metadata(res_s2)
                
                # Figure validation
                is_fig = (hasattr(res_s2, 'canvas') or 'matplotlib.figure.Figure' in str(type(res_s2)))
                
                if res_s2 is None or not is_fig or meta2 in ["EMPTY_FIG", "NO_DATA"]:
                    none_ret = True
                elif meta1 == meta2:
                    h_det = True
                else:
                    p_ok = True
                
                expected_res = "Dynamic matplotlib.figure.Figure"
                actual_res = f"Figure Content: {meta2}"
            elif i == 1:
                res_s = run_t(i, StudentClass, ([1,2,3], 0, []))
                p_ok = (res_s == 3)
                expected_res = 3
                actual_res = res_s
            else:
                s_raw = [10.0, 20.0, 30.0]
                if i == 2 or i == 5: s_raw[0] = 500.0
                s_params = (s_raw, 15.0, s_raw)
                
                res_s1 = run_t(i, StudentClass, s_params)
                res_s2 = run_t(i, StudentClass, params)
                res_r2 = run_t(i, ReferenceClass, params) # Fixed: idx was missing
                
                if compare_results(res_s2, res_r2): p_ok = True
                elif res_s2 is None or res_s2 in [[], {}, 0.0, 0, ""]: none_ret = True
                elif res_s1 == res_s2: h_det = True
                
                expected_res = res_r2
                actual_res = res_s2

            if p_ok:
                total_score += marks
                msg = f"PASS TC{i} [{desc}] ({marks}/{marks})"
            elif none_ret:
                msg = f"FAIL TC{i} [{desc}] (0/{marks}) - Method not implemented / No return value"
            elif h_det:
                msg = f"FAIL TC{i} [{desc}] (0/{marks}) - Hardcoded. Dynamic check failed."
            else:
                msg = f"FAIL TC{i} [{desc}] (0/{marks}) - Incorrect Output. Expected non-empty dynamic results."
                
        except Exception as e: msg = f"FAIL TC{i} [{desc}] | Error: {e}"
        print(msg); report_lines.append(msg)

    score_line = f"\nSCORE: {total_score}/20.0"
    print(score_line); report_lines.append(score_line)
    with open(report_path, "w", encoding="utf-8") as f: f.write("\n".join(report_lines) + "\n")

def compare_results(r, e):
    try:
        if r == e: return True
        if isinstance(r, (float, int)): return round(float(r), 1) == round(float(e), 1)
        if isinstance(r, dict):
            if len(r) != len(e): return False
            return all(k in r and compare_results(r[k], e[k]) for k in e)
        if isinstance(r, list):
            if len(r) != len(e): return False
            return all(compare_results(x, y) for x, y in zip(r, e))
        return str(r).strip() == str(e).strip()
    except: return False

if __name__ == "__main__":
    import sys
    sol_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(sol_file)
