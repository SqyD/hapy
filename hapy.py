# A opython client library for Home Assistant.
import json

# Import a version of requests.
# Starts with circuit python, then micropython, then plain python.
try:
    import adafruit_requests as requests
except ImportError:
    try:
        import urequests as requests
    except ImportError:
        import requests

# Define a Home Assistant Client.

class HAClient:
    def __init__(self, url, access_token = ''):
        # Set the client configuration.
        self.url = url
        self.access_token = access_token

    def test_auth(self):
        if self.access_token == '':
            return False
        else:
            test_response = self.ha_request("GET", "/api/")
        if test_response.status_code == 200 or test_response.status_code == 201:
            return True
        else:
            return False

    def register(self, regdata):
        response = self.ha_request(
            method = "POST",
            path = "/api/mobile_app/registrations",
            data = app_registration
        )

    def ha_request(self, method, path, data = ''):
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/json',
        }
        if method == "POST":
            response = requests.post(self.url + path, data = data, headers = headers)
        elif method == "GET":
            response = requests.get(self.url + path, headers = headers)
        return response

    def get_state(self, entity_id):
        response = self.ha_request("GET", "/api/states/" + entity_id)
        state = json.loads(response.text)
        response.close()
        return state

    def set_state(self, entity_id, state):
        response = self.ha_request("POST", "/api/states/" + entity_id, data = json.dumps(state))
        state = json.loads(response.text)
        return state

    def call_service(self, service, data):
        path = "/api/services/" + service.replace(".", "/", 1)
        response = self.ha_request("POST", path, data = json.dumps(data))
        states = json.loads(response.text)
        response.close()
        return states
