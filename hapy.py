# A simple python client library for Home Assistant.
# Found at https://github.com/SqyD/hapy
import time

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

# A generic superclass to manage entity state.

class HaPy:
    def __init__(self):
        self.entity_cache = dict()

    def entity_cache_iscached(self, entity_id):
        if entity_id in self.entity_cache:
            if self.entity_cache_isexpired(entity_id):
                self.entity_cache_expire(entity_id)
                return False
            else:
                return True
        else:
            return False

    def entity_cache_isexpired(self, entity_id):
        expired = self.entity_cache[entity_id]['updated'] + self.entity_cache[entity_id]['ttl'] < time.time()
        return expired

    def entity_cache_set(self, entity_id, entity_data, ttl = 30):
        if not entity_id in self.entity_cache:
            self.entity_cache[entity_id] = dict()
        self.entity_cache[entity_id]['data'] = entity_data
        self.entity_cache[entity_id]['updated'] = time.time()
        if not ttl in self.entity_cache[entity_id]:
            self.entity_cache[entity_id]['ttl'] = ttl

    def entity_cache_expire(self, entity_id):
        if entity_id in self.entity_cache:
            del self.entity_cache[entity_id]

    def entity_get(self, entity_id):
        if self.entity_cache_iscached(entity_id):
            entity_data = self.entity_cache[entity_id]['data']
        else:
            entity_data = False
        return entity_data

    def entity_get_state(self, entity_id):
        entity = self.entity_get(entity_id)
        state = entity['state']
        return state

    def entity_get_attr(self, entity_id, attr):
        entity = self.entity_get(entity_id)
        value = entity['attributes'][attr]
        return value
# Define a Home Assistant Client.

class HaPyRest(HaPy):
    def __init__(self, secrets = dict()):
        super().__init__()
        self.url = secrets['url']
        self.access_token = secrets['access_token']

    def test_auth(self):
        if self.access_token == '':
            return False
        else:
            test_response = self.ha_request("GET", "/api/")
            if test_response['message'] == "API running.":
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
        # First try getting the data from cache
        cache = super().entity_get(entity_id)
        if cache:
            entity_data = cache
        else:
            # If not in cache, get it from Home Assistant
            entity_data = self.ha_request("GET", "/api/states/" + entity_id)
            self.entity_cache_set(entity_id, entity_data)
        return entity_data

    def entity_set(self, entity_id, state_data):
        state = self.ha_request("POST", "/api/states/" + entity_id, data = json.dumps(state_data))
        # self.entity_cache_expire(entity_id)
        return state

    def entity_set_state(self, entity_id, state):
        state_data = dict()
        state_data['state'] = state
        state = self.entity_set(entity_id, state_data)
        return state

    def call_service(self, service, data):
        path = "/api/services/" + service.replace(".", "/", 1)
        states = self.ha_request("POST", path, data = json.dumps(data))
        if entity_id in data:
            self.entity_cache_expire(data['entity_id'])
        return states

    def register(self, regdata):
        response = self.ha_request(
            method = "POST",
            path = "/api/mobile_app/registrations",
            data = app_registration
        )
