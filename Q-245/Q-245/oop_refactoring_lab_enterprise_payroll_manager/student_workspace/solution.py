import sys

class Employee:
    def __init__(self, emp_id, base_salary, bonus):
        # Implementation here
        pass

class PayrollRefactorer:
    def __init__(self):
        # Implementation here: use a list of Employee objects
        pass

    def add_employee(self, emp_id, base, bonus):
        # Implementation here
        pass

    def calculate_total_payout(self) -> float:
        # Implementation here
        pass

    def get_top_earner(self) -> str:
        # Implementation here
        pass

    def generate_report(self) -> dict:
        # Implementation here
        pass

if __name__ == "__main__":
    # Command processor for standardized evaluation
    manager = PayrollRefactorer()
    input_data = sys.stdin.read().splitlines()
    for line in input_data:
        parts = line.strip().split()
        if not parts: continue
        cmd = parts[0]
        if cmd == "ADD": manager.add_employee(parts[1], parts[2], parts[3])
        elif cmd == "REPORT":
            rep = manager.generate_report()
            print(f"Count: {rep['count']}")
            print(f"Total: {rep['total_payout']:.1f}")
            print(f"Top: {rep['top_earner']}")
