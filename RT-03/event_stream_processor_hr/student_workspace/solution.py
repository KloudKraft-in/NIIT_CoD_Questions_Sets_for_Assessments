from typing import List, Dict, Generator, Optional, Any, Set, Tuple
import json
from collections import defaultdict, Counter
import sys

# Complete the 'processEventStream' function below.
#
# The function is expected to yield results in batches.
# Deduplicate events by 'event_id' (keep the earliest timestamp).

def processEventStream(
    events: List[Tuple[str, int, str, str]], 
    event_types: Optional[Set[str]] = None, 
    window_seconds: Optional[int] = None,
    batch_size: Optional[int] = None
) -> Generator: 

    """ WRITE YOUR CODE HERE """
    
    

    pass

#Don't make any changes in below code.
if __name__ == '__main__':
    # Standard input reading for a JSON block representing the stream
    input_text = sys.stdin.read().strip()
    if input_text:
        data = json.loads(input_text)
        events = data.get("events", [])
        event_types_raw = data.get("event_types")
        event_types = set(event_types_raw) if event_types_raw is not None else None
        window_seconds = data.get("window_seconds")
        batch_size = data.get("batch_size")
        
        # Execute and print batches
        for batch in processEventStream(events, event_types, window_seconds, batch_size):
            print(json.dumps(batch, sort_keys=True))
