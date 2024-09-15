from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

class InventoryService:
    def __init__(self):
        self.inventory = {}
        self.server_running = False
        self.logger = logging.getLogger('InventoryService')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def start_server(self):
        if not self.server_running:
            self.server_running = True
            self.logger.info("Server started.")
            return "Server started."
        else:
            self.logger.warning("Server is already running.")
            return "Server is already running."

    def stop_server(self):
        if self.server_running:
            self.server_running = False
            self.logger.info("Server stopped.")
            return "Server stopped."
        else:
            self.logger.warning("Server is not running.")
            return "Server is not running."

    def define_stuff(self, type, description):
        if not self.server_running:
            self.logger.error("Server is not running. Cannot define stuff.")
            return "Server is not running. Cannot define stuff."
        
        if type in self.inventory:
            self.logger.warning(f"Type '{type}' is already defined.")
            return f"Type '{type}' is already defined."
        else:
            self.inventory[type] = {'description': description, 'quantity': 0}
            self.logger.info(f"Defined type '{type}' with description '{description}'.")
            return f"Defined type '{type}' with description '{description}'."

    def undefine(self, type):
        if not self.server_running:
            self.logger.error("Server is not running. Cannot undefine stuff.")
            return "Server is not running. Cannot undefine stuff."
        
        if type in self.inventory:
            del self.inventory[type]
            self.logger.info(f"Undefined type '{type}'.")
            return f"Undefined type '{type}'."
        else:
            self.logger.warning(f"Type '{type}' does not exist.")
            return f"Type '{type}' does not exist."

    def add(self, N, type):
        if not self.server_running:
            self.logger.error("Server is not running. Cannot add stuff.")
            return "Server is not running. Cannot add stuff."
        
        if type in self.inventory:
            self.inventory[type]['quantity'] += N
            self.logger.info(f"Added {N} of type '{type}'.")
            return f"Added {N} of type '{type}'."
        else:
            self.logger.warning(f"Type '{type}' does not exist.")
            return f"Type '{type}' does not exist."

    def remove(self, N, type):
        if not self.server_running:
            self.logger.error("Server is not running. Cannot remove stuff.")
            return "Server is not running. Cannot remove stuff."
        
        if type in self.inventory:
            if self.inventory[type]['quantity'] >= N:
                self.inventory[type]['quantity'] -= N
                self.logger.info(f"Removed {N} of type '{type}'.")
                return f"Removed {N} of type '{type}'."
            else:
                self.logger.warning(f"Not enough of type '{type}' to remove.")
                return f"Not enough of type '{type}' to remove."
        else:
            self.logger.warning(f"Type '{type}' does not exist.")
            return f"Type '{type}' does not exist."

# Create an instance of InventoryService
service = InventoryService()

@app.route('/start_server', methods=['POST'])
def start_server():
    result = service.start_server()
    return jsonify({'message': result})

@app.route('/stop_server', methods=['POST'])
def stop_server():
    result = service.stop_server()
    return jsonify({'message': result})

@app.route('/define_stuff', methods=['POST'])
def define_stuff():
    data = request.json
    type = data.get('type')
    description = data.get('description')
    result = service.define_stuff(type, description)
    return jsonify({'message': result})

@app.route('/undefine', methods=['POST'])
def undefine():
    data = request.json
    type = data.get('type')
    result = service.undefine(type)
    return jsonify({'message': result})

@app.route('/add', methods=['POST'])
def add():
    data = request.json
    N = data.get('quantity')
    type = data.get('type')
    result = service.add(N, type)
    return jsonify({'message': result})

@app.route('/remove', methods=['POST'])
def remove():
    data = request.json
    N = data.get('quantity')
    type = data.get('type')
    result = service.remove(N, type)
    return jsonify({'message': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

