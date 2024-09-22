import logging
import json
import os

class InventoryService:
    def __init__(self):
        self.inventory = {}
        self.current_snapshot_id = 0
        self.snapshots = {}  
        self.logger = logging.getLogger('InventoryService')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def define_stuff(self, type, description):
        if type in self.inventory:
            self.logger.warning(f"Type '{type}' is already defined.")
            return f"Type '{type}' is already defined."
        else:
            self.inventory[type] = {'description': description, 'quantity': 0}
            self.logger.info(f"Defined type '{type}' with description '{description}'.")
            return f"Defined type '{type}' with description '{description}'."

    def undefine(self, type):
        if type in self.inventory:
            del self.inventory[type]
            self.logger.info(f"Undefined type '{type}'.")
            return f"Undefined type '{type}'."
        else:
            self.logger.warning(f"Type '{type}' does not exist.")
            return f"Type '{type}' does not exist."

    def add(self, quantity, type):
        if type in self.inventory:
            self.inventory[type]['quantity'] += quantity
            self.logger.info(f"Added {quantity} of type '{type}'.")
            return f"Added {quantity} of type '{type}'."
        else:
            self.logger.warning(f"Type '{type}' does not exist.")
            return f"Type '{type}' does not exist."

    def remove(self, quantity, type):
        if type in self.inventory:
            if self.inventory[type]['quantity'] >= quantity:
                self.inventory[type]['quantity'] -= quantity
                self.logger.info(f"Removed {quantity} of type '{type}'.")
                return f"Removed {quantity} of type '{type}'."
            else:
                self.logger.warning(f"Not enough of type '{type}' to remove.")
                return f"Not enough of type '{type}' to remove."
        else:
            self.logger.warning(f"Type '{type}' does not exist.")
            return f"Type '{type}' does not exist."

    def get_count(self, type):
        if type in self.inventory:
            return self.inventory[type]['quantity']
        else:
            return -1
        
        # adding the new methods
    def save_data(self):
        snapshot_id = self.current_snapshot_id
        self.snapshots[snapshot_id] = json.dumps(self.inventory)
        self.current_snapshot_id += 1
        return snapshot_id

    def load_data(self, snapshot_id):
        if snapshot_id in self.snapshots:
            self.inventory = json.loads(self.snapshots[snapshot_id])
            return 0
        return -1

    def delete_data(self, snapshot_id):
        if snapshot_id in self.snapshots:
            del self.snapshots[snapshot_id]
            return 0
        return -1

