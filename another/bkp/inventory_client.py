import requests
import json

class InventoryClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def _post(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers, data=json.dumps(data) if data else None)
        response.raise_for_status()
        return response.json()

    def start_server(self):
        return self._post('start_server')

    def stop_server(self):
        return self._post('stop_server')

    def define_stuff(self, type, description):
        return self._post('define_stuff', {"type": type, "description": description})

    def undefine(self, type):
        return self._post('undefine', {"type": type})

    def add(self, quantity, type):
        return self._post('add', {"quantity": quantity, "type": type})

    def remove(self, quantity, type):
        return self._post('remove', {"quantity": quantity, "type": type})

# Example usage
if __name__ == "__main__":
    client = InventoryClient("http://localhost:5000")
    
    print(client.start_server())
    print(client.define_stuff("widget", "A useful widget"))
    print(client.add(10, "widget"))
    print(client.remove(5, "widget"))
    print(client.undefine("widget"))
    print(client.stop_server())

