import logging

class InventoryService:
    def __init__(self):
        self.inventory = {}
        self.server_running = False
        # Setting up the logger
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
        else:
            self.logger.warning("Server is already running.")

    def stop_server(self):
        if self.server_running:
            self.server_running = False
            self.logger.info("Server stopped.")
        else:
            self.logger.warning("Server is not running.")

    def define_stuff(self, type, description):
        if not self.server_running:
            self.logger.error("Server is not running. Cannot define stuff.")
            return
        
        if type in self.inventory:
            self.logger.warning(f"Type '{type}' is already defined.")
        else:
            self.inventory[type] = {'description': description, 'quantity': 0}
            self.logger.info(f"Defined type '{type}' with description '{description}'.")

    def undefine(self, type):
        if not self.server_running:
            self.logger.error("Server is not running. Cannot undefine stuff.")
            return
        
        if type in self.inventory:
            del self.inventory[type]
            self.logger.info(f"Undefined type '{type}'.")
        else:
            self.logger.warning(f"Type '{type}' does not exist.")

    def add(self, N, type):
        if not self.server_running:
            self.logger.error("Server is not running. Cannot add stuff.")
            return
        
        if type in self.inventory:
            self.inventory[type]['quantity'] += N
            self.logger.info(f"Added {N} of type '{type}'.")
        else:
            self.logger.warning(f"Type '{type}' does not exist.")

    def remove(self, N, type):
        if not self.server_running:
            self.logger.error("Server is not running. Cannot remove stuff.")
            return
        
        if type in self.inventory:
            if self.inventory[type]['quantity'] >= N:
                self.inventory[type]['quantity'] -= N
                self.logger.info(f"Removed {N} of type '{type}'.")
            else:
                self.logger.warning(f"Not enough of type '{type}' to remove.")
        else:
            self.logger.warning(f"Type '{type}' does not exist.")

# Example usage:
if __name__ == "__main__":
    service = InventoryService()
    service.start_server()
    service.define_stuff("widget", "A useful widget")
    service.add(10, "widget")
    service.remove(5, "widget")
    service.undefine("widget")
    service.stop_server()

