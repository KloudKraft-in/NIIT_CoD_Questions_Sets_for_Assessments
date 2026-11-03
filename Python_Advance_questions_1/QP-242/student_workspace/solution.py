import requests

class APIError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

class APIHandler:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def fetch_data(self, endpoint: str) -> dict:
       # TODO: Perform GET request to base_url + endpoint
       # If status 200: return JSON data
       # If status 404: raise APIError(404, "Not Found")

        """ WRITE YOUR CODE HERE """

    def submit_data(self, endpoint: str, payload: dict) -> str:
       # TODO: Perform POST request with JSON payload
       # If status 201: return "Created"
       # If status 400: return "Bad Request"

       """ WRITE YOUR CODE HERE """

    def get_user_email(self, user_id: int) -> str:
        try:
            data = self.fetch_data(f"/users/{user_id}")
            return data.get("email", "No Email Found")
        except APIError as e:
            if e.status_code == 404:
                return "User Not Found"
            return "API Error"