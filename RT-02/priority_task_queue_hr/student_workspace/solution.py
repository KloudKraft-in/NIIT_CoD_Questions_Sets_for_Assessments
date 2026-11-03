from typing import List, Dict, Optional, Tuple, Callable
from functools import wraps
import json
import sys

# Complete the 'TaskQueue' class below.
#
# The class is expected to manage task priorities and dependencies.

def validate_task_data(func: Callable) -> Callable:
    """Decorator to validate task and priority data"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Validation logic can be added here
        return func(*args, **kwargs)
    return wrapper

class TaskQueue:
    """Core logic for managing prioritized tasks with dependencies"""
    def __init__(self):
        # Initialize internal structures
        pass

    @validate_task_data
    def add_task(self, task_id: str, priority: int, dependencies: List[str]) -> None:
        """Adds a new task to the queue"""
        pass

    def is_ready(self, task_id: str) -> bool:
        """Returns True if all dependencies of the task are completed"""
        return False

    def complete_task(self, task_id: str) -> None:
        """Marks a task as completed"""
        pass

    def get_status(self, task_id: str) -> str:
        """Returns the current status of the task"""
        return "unknown"

    def get_ready_tasks(self) -> List[str]:
        """Returns a list of tasks that are ready to be processed"""
        return []

    def get_next(self) -> Optional[str]:
        """Returns the next task to process"""
        return None

#NOTE : Dont modify below code.
def main():
    """HackerRank-style driver for processing operations"""
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
    
    n_ops = int(input_data[0].strip())
    tq = TaskQueue()

    for i in range(1, n_ops + 1):
        line = input_data[i].strip().split(' ', 1)
        if not line: continue
        cmd = line[0]
        args_str = line[1] if len(line) > 1 else ""

        if cmd == "add_task":
            # Expecting: task_id priority [json_deps]
            parts = args_str.split(' ', 2)
            task_id = parts[0]
            priority = int(parts[1])
            deps = json.loads(parts[2])
            tq.add_task(task_id, priority, deps)
        elif cmd == "is_ready":
            print(str(tq.is_ready(args_str.strip())).lower())
        elif cmd == "complete_task":
            tq.complete_task(args_str.strip())
        elif cmd == "get_next":
            res = tq.get_next()
            print(res if res else "None")
        elif cmd == "get_status":
            print(tq.get_status(args_str.strip()))
        elif cmd == "get_ready_tasks":
            print(",".join(tq.get_ready_tasks()))

if __name__ == '__main__':
    main()
