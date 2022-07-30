# A simple python client library for Home Assistant.
# Found at https://github.com/SqyD/hapy

try:
    import ujson as json
except ImportError:
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
            if test_response['message'] == "API running":
                return True
            else:
                return False

    def ha_request(self, method, path, data = ''):
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/json',
        }
        if method == "POST":
            response = requests.post(self.url + path, data = data, headers = headers)
        elif method == "GET":
            response = requests.get(self.url + path, headers = headers)
        data = json.loads(response.text)
        response.close()
        return data

    def entity_get(self, entity_id):
        entity = self.ha_request("GET", "/api/states/" + entity_id)
        return entity

    def entity_get_state(self, entity_id):
        entity = self.entity_get(entity_id)
        state = entity['state']
        return state

    def entity_set(self, entity_id, state_data):
        state = self.ha_request("POST", "/api/states/" + entity_id, data = json.dumps(state_data))
        return state

    def entity_set_state(self, entity_id, state):
        state_data = dict()
        state_data['state'] = state
        state = self.entity_set(entity_id, state_data)
        return state

    def call_service(self, service, data):
        path = "/api/services/" + service.replace(".", "/", 1)
        states = self.ha_request("POST", path, data = json.dumps(data))
        return states

    def register(self, regdata):
        response = self.ha_request(
            method = "POST",
            path = "/api/mobile_app/registrations",
            data = app_registration
        )
