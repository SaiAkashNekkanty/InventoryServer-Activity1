import requests
import json

class InventoryClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def _post(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers, data=json.dumps(data) if data is not None else json.dumps({}))
        response.raise_for_status()
        return response.json()

    def _get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def define_stuff(self, type, description):
        return self._post('define_stuff', {"type": type, "description": description})

    def undefine(self, type):
        return self._post('undefine', {"type": type})

    def add(self, quantity, type):
        return self._post('add', {"quantity": quantity, "type": type})

    def remove(self, quantity, type):
        return self._post('remove', {"quantity": quantity, "type": type})

    def get_count(self, type):
        return self._get('get_count', params={"type": type})
    
    # Adding new methods for the Assignment 2

    def save_data(self):
        response = self._post('save_data', {})
        return response.get('id')

    def load_data(self, snapshot_id):
        return self._post('load_data', {"id": snapshot_id})

    def delete_data(self, snapshot_id):
        return self._post('delete_data', {"id": snapshot_id})
    
# Example usage
if __name__ == "__main__":
    client = InventoryClient("http://localhost:5000")
    
    print(client.define_stuff("widget", "A useful widget"))
    print(client.add(10, "widget"))
    print(client.remove(5, "widget"))
    print(client.get_count("widget"))
    print(client.undefine("widget"))
