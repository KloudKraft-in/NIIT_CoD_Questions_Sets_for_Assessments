#student_workspace/solution.py

class EventAPISimulator:
    def __init__(self):
        self.events = {}  # {id: name}
        self.logs = []    # ["[LEVEL]: Message"]

    def post_event(self, event_id: int, name: str) -> dict:
     """ YOUR CODE HERE """
        return {"status": 201, "message": "Created"}

    def get_event(self, event_id: int) -> dict:
        """" YOUR CODE HERE """
        return {"status": 404, "message": "Not Found"}

    def put_event(self, event_id: int, new_name: str) -> dict:
        """ YOUR CODE HERE """
        return {"status": 404, "message": "Not Found"}

    def delete_event(self, event_id: int) -> dict:
        """ YOUR CODE HERE"""
            return {"status": 200, "message": "Deleted"}
        return {"status": 404, "message": "Not Found"}

    def search_events(self, query: str) -> list:
        """ YOUR CODE HERE """
        return [eid for eid, name in self.events.items() if query in name.lower()]

    def get_logs_by_level(self, level: str) -> list:
        """ YOUR CODE HERE """
        return [L for L in self.logs if L.startswith(prefix)]

    def get_api_usage_stats(self) -> dict:
        """YOUR CODE HERE"""
