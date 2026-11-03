import sys
import json

class APIError(Exception):
    def __init__(self, status_code, message):
        # Implementation here
        pass

class APIHandler:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.mock_db = {} 

    def _mock_request(self, method, endpoint, payload=None):
        # DO NOT CHANGE: Utility for local testing
        if endpoint in self.mock_db: return self.mock_db[endpoint]
        return (404, {"error": "Not Found"})

    def fetch_data(self, endpoint: str) -> dict:
        # Implementation here: Use _mock_request to simulate GET
        pass

    def submit_data(self, endpoint: str, payload: dict) -> str:
        # Implementation here: Use _mock_request to simulate POST
        pass

    def get_user_email(self, user_id: int) -> str:
        # Implementation here: Use fetch_data
        pass

if __name__ == "__main__":
    # Command processor for standardized evaluation
    handler = APIHandler("http://api.local")
    input_data = sys.stdin.read().splitlines()
    for line in input_data:
        parts = line.strip().split(maxsplit=2)
        if not parts: continue
        cmd = parts[0]
        if cmd == "MOCK":
            endpoint = parts[1]
            status_json = parts[2].split(maxsplit=1)
            handler.mock_db[endpoint] = (int(status_json[0]), json.loads(status_json[1]))
        elif cmd == "FETCH":
            try: print(json.dumps(handler.fetch_data(parts[1]), sort_keys=True))
            except APIError as e: print(f"ERROR: {e.message}")
        elif cmd == "SUBMIT":
            print(handler.submit_data(parts[1], json.loads(parts[2])))
        elif cmd == "USER_EMAIL":
            print(handler.get_user_email(int(parts[1])))