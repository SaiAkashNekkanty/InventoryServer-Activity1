import requests
import json
import os


def locator(type):
    environment = os.getenv('ENVIRONMENT', 'local') 

    if environment == 'docker':
        if type[0].lower() >= 'a' and type[0].lower() <= 'l':
            return 'http://server_a:5000'
        else:
            return 'http://server_b:5000'
    else:
        if type[0].lower() >= 'a' and type[0].lower() <= 'l':
            return 'http://localhost:5001'
        else:
            return 'http://localhost:5002'

class InventoryClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def _post(self, url, endpoint, data=None):
        full_url = f"{url}/{endpoint}"
        headers = {"Content-Type": "application/json"}
        response = requests.post(full_url, headers=headers, data=json.dumps(data) if data else None)
        response.raise_for_status()
        return response.json()

    def _get(self, url, endpoint, params=None):
        full_url = f"{url}/{endpoint}"
        response = requests.get(full_url, params=params)
        response.raise_for_status()
        return response.json()

    def define_stuff(self, type, description):
        url = locator(type)  
        return self._post(url, 'define_stuff', {"type": type, "description": description})

    def undefine(self, type):
        url = locator(type)  
        return self._post(url, 'undefine', {"type": type})

    def add(self, quantity, type):
        url = locator(type)  
        return self._post(url, 'add', {"quantity": quantity, "type": type})

    def remove(self, quantity, type):
        url = locator(type)  
        return self._post(url, 'remove', {"quantity": quantity, "type": type})

    def get_count(self, type):
        url = locator(type)  
        return self._get(url, 'get_count', params={"type": type})

    def save_data(self):
        return self._post(self.base_url, 'save_data')

    def load_data(self, snapshot_id):
        return self._post(self.base_url, 'load_data', {"snapshot_id": snapshot_id})

    def delete_data(self, snapshot_id):
        return self._post(self.base_url, 'delete_data', {"snapshot_id": snapshot_id})

    # New functions for A4
    def get_server1_name(self):
        return 'server_a'

    def get_server2_name(self):
        return 'server_b'

if __name__ == "__main__":
    client = InventoryClient("http://localhost:5000")
    
    print(client.define_stuff("widget", "A useful widget"))
    print(client.add(10, "widget"))
    print(client.remove(5, "widget"))
    print(client.get_count("widget"))
    print(client.save_data())  
    print(client.load_data("1")) 
    print(client.undefine("widget"))
