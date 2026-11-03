import importlib.util
import os
import sys
import random

class ReferenceEventAPISimulator:
    def __init__(self):
        self.events = {}  # {id: name}
        self.logs = []    # ["[LEVEL]: Message"]

    def post_event(self, event_id: int, name: str) -> dict:
        self.events[event_id] = name
        self.logs.append(f"INFO: Created {event_id}")
        return {"status": 201, "message": "Created"}

    def get_event(self, event_id: int) -> dict:
        if event_id in self.events:
            return {"status": 200, "data": self.events[event_id]}
        self.logs.append(f"WARNING: Not Found {event_id}")
        return {"status": 404, "message": "Not Found"}

    def put_event(self, event_id: int, new_name: str) -> dict:
        if event_id in self.events:
            self.events[event_id] = new_name
            self.logs.append(f"INFO: Updated {event_id}")
            return {"status": 200, "message": "Updated"}
        return {"status": 404, "message": "Not Found"}

    def delete_event(self, event_id: int) -> dict:
        if event_id in self.events:
            del self.events[event_id]
            self.logs.append(f"INFO: Deleted {event_id}")
            return {"status": 200, "message": "Deleted"}
        return {"status": 404, "message": "Not Found"}

    def search_events(self, query: str) -> list:
        query = query.lower()
        self.logs.append(f"INFO: Search {query}")
        return [eid for eid, name in self.events.items() if query in name.lower()]

    def get_logs_by_level(self, level: str) -> list:
        prefix = f"{level.upper()}:"
        return [L for L in self.logs if L.startswith(prefix)]

    def get_api_usage_stats(self) -> dict:
        return {
            "total_events": len(self.events),
            "total_logs": len(self.logs)
        }

def test_student_code(solution_path):
    report_dir = os.path.dirname(solution_path)
    report_path = os.path.join(report_dir, "report.txt")
    
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    try: spec.loader.exec_module(solution)
    except Exception as e:
        print(f"IMPORT ERROR: {e}"); return

    print("Running Tests for: RESTful Event API Simulator (Independence & Unique Methods Mode)\n")
    report_lines = ["Running Tests for: RESTful Event API Simulator (Independence & Unique Methods Mode)\n"]

    if not hasattr(solution, "EventAPISimulator"):
        print("ERROR: EventAPISimulator class not found"); return
    
    StudentClass = solution.EventAPISimulator
    ReferenceClass = ReferenceEventAPISimulator
    
    tc_configs = [
        ("Verification of basic POST operation", 0),
        ("Retrieve event with 404 warning log", 3),
        ("Successfully update event title (PUT)", 3),
        ("Correctly delete event resource", 3),
        ("Filter events by name substring (Search)", 3),
        ("Filter diagnostic logs by level", 4),
        ("Aggregate API usage statistics", 4),
    ]

    random.seed(None)
    total_score = 0
    
    for i, (desc, marks) in enumerate(tc_configs, 1):
        try:
            def run_t(idx, cls_to_use, data_params):
                eid, name, extra = data_params
                obj = cls_to_use()
                obj.post_event(101, "Initial Event") # Setup
                
                if idx == 1: 
                    t_obj = cls_to_use()
                    if not hasattr(t_obj, 'events'): return "MISSING_ATTR"
                    return t_obj.events
                
                if idx == 2: 
                    res1 = obj.get_event(101)
                    res2 = obj.get_event(999)
                    return [res1, res2, obj.logs]
                
                if idx == 3: 
                    res = obj.put_event(101, name)
                    return [res, obj.events]
                
                if idx == 4: 
                    res = obj.delete_event(101)
                    return [res, obj.events]
                
                if idx == 5: 
                    obj.post_event(102, name)
                    return obj.search_events(extra)
                
                if idx == 6: 
                    obj.get_event(999) # Generate Warning
                    return obj.get_logs_by_level(extra)
                
                if idx == 7: 
                    obj.post_event(102, "Extra")
                    return obj.get_api_usage_stats()
                
                return None

            p_ok, h_det, none_ret = False, False, False
            
            if i == 1:
                actual_res = run_t(i, StudentClass, (0, "", ""))
                expected_res = {}
                p_ok = (actual_res == expected_res)
            else:
                # DUAL RUN for random/dynamic check
                rv_id = random.randint(200, 500)
                rv_name = f"Event_{random.randint(1000, 9999)}"
                rv_search = "event"
                
                # Dynamic Parameters
                params = (rv_id, rv_name, rv_search)
                
                # RUN Students
                res_s1 = run_t(idx=i, cls_to_use=StudentClass, data_params=(102, "Cloud Workshop", "cloud"))
                res_s2 = run_t(idx=i, cls_to_use=StudentClass, data_params=params)
                
                # RUN Reference
                res_r1 = run_t(idx=i, cls_to_use=ReferenceClass, data_params=(102, "Cloud Workshop", "cloud"))
                res_r2 = run_t(idx=i, cls_to_use=ReferenceClass, data_params=params)
                
                if compare_results(res_s2, res_r2):
                    p_ok = True
                elif res_s2 is None:
                    none_ret = True
                elif res_s1 == res_s2:
                    h_det = True

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
                msg = f"FAIL TC{i} [{desc}] (0/{marks}) - Incorrect Output. Expected: {expected_res} | Actual: {actual_res}"
                
        except Exception as e: msg = f"FAIL TC{i} [{desc}] | Error: {e}"
        print(msg); report_lines.append(msg)

    score_line = f"\nSCORE: {total_score}/20.0"
    print(score_line); report_lines.append(score_line)
    with open(report_path, "w", encoding="utf-8") as f: f.write("\n".join(report_lines) + "\n")

def compare_results(r, e):
    try:
        if isinstance(r, (float, int)): return round(float(r), 1) == round(float(e), 1)
        if isinstance(r, dict):
            if len(r) != len(e): return False
            for k in e:
                if k not in r: return False
                if not compare_results(r[k], e[k]): return False
            return True
        if isinstance(r, list):
            if len(r) != len(e): return False
            return all(compare_results(x, y) for x, y in zip(r, e))
        return str(r).strip() == str(e).strip()
    except: return False

if __name__ == "__main__":
    import sys
    sol_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(sol_file)
