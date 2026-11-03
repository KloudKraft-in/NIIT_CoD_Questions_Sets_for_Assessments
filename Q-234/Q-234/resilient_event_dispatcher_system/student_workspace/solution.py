import sys
import json

class EventDispatcher:
    def __init__(self):
        # Implementation here
        pass

    def subscribe(self, event_type: str, callback):
        # Implementation here
        pass

    def unsubscribe(self, event_type: str, callback):
        # Implementation here
        pass

    def dispatch(self, event_type: str, data: dict):
        # Implementation here
        pass

if __name__ == "__main__":
    # Command processor for standardized evaluation
    dispatcher = EventDispatcher()
    
    def log_event(data):
        print(f"Log: {data.get('message', 'No message')}")
    def process_data(data):
        if data.get('fail'): raise ValueError("Processing failed")
        print(f"Process: {data.get('id', 0)}")
    callbacks = {"log_event": log_event, "process_data": process_data}

    input_data = sys.stdin.read().splitlines()
    for line in input_data:
        parts = line.strip().split(maxsplit=2)
        if not parts: continue
        cmd = parts[0]
        if cmd == "SUBSCRIBE":
            dispatcher.subscribe(parts[1], callbacks[parts[2]])
        elif cmd == "UNSUBSCRIBE":
            dispatcher.unsubscribe(parts[1], callbacks[parts[2]])
        elif cmd == "DISPATCH":
            data = json.loads(parts[2])
            dispatcher.dispatch(parts[1], data)
