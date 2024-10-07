import json
import os
import logging

class InventoryService:
    def __init__(self):
        self.inventory = {}
        self.snapshots = {} 
        logging.basicConfig(level=logging.INFO)

    def define_stuff(self, item_type, description):
        if item_type in self.inventory:
            logging.warning(f"Type '{item_type}' is already defined.")
            return f"Type '{item_type}' is already defined."
        else:
            self.inventory[item_type] = {'description': description, 'quantity': 0}
            logging.info(f"Defined type '{item_type}' with description '{description}'.")
            return f"Defined type '{item_type}' with description '{description}'."

    def undefine(self, item_type):
        if item_type in self.inventory:
            del self.inventory[item_type]
            logging.info(f"Undefined type '{item_type}'.")
            return f"Undefined type '{item_type}'."
        else:
            logging.warning(f"Type '{item_type}' does not exist.")
            return f"Type '{item_type}' does not exist."

    def add(self, quantity, item_type):
        if item_type in self.inventory:
            self.inventory[item_type]['quantity'] += quantity
            logging.info(f"Added {quantity} of type '{item_type}'.")
            return f"Added {quantity} of type '{item_type}'."
        else:
            logging.warning(f"Type '{item_type}' does not exist.")
            return f"Type '{item_type}' does not exist."

    def remove(self, quantity, item_type):
        if item_type in self.inventory:
            if self.inventory[item_type]['quantity'] >= quantity:
                self.inventory[item_type]['quantity'] -= quantity
                logging.info(f"Removed {quantity} of type '{item_type}'.")
                return f"Removed {quantity} of type '{item_type}'."
            else:
                logging.warning(f"Not enough of type '{item_type}' to remove.")
                return f"Not enough of type '{item_type}' to remove."
        else:
            logging.warning(f"Type '{item_type}' does not exist.")
            return f"Type '{item_type}' does not exist."

    def get_count(self, item_type):
        if item_type in self.inventory:
            count = self.inventory[item_type]['quantity']
            logging.info(f"Count for '{item_type}': {count}.")
            return count
        else:
            logging.info(f"Count for '{item_type}': -1 (undefined).")
            return -1

    def save_data(self):
        snapshot_id = str(len(self.snapshots) + 1)  
        filename = f'snapshot_{snapshot_id}.json'  

        with open(filename, 'w') as f:
            json.dump(self.inventory, f)

        self.snapshots[snapshot_id] = filename  
        return {'snapshot_id': snapshot_id}

    def load_data(self, snapshot_id):
        filename = self.snapshots.get(snapshot_id) 
        if not filename or not os.path.exists(filename):
            logging.error(f"Snapshot ID '{snapshot_id}' not found.")
            return 404  

        with open(filename, 'r') as f:
            self.inventory = json.load(f)

        logging.info(f"Loaded inventory from snapshot ID '{snapshot_id}'.")
        return 0  

    def delete_data(self, snapshot_id):
        filename = self.snapshots.pop(snapshot_id, None) 
        if filename and os.path.exists(filename):
            os.remove(filename) 
            logging.info(f"Deleted snapshot ID '{snapshot_id}'.")
            return 0 
        logging.error(f"Snapshot ID '{snapshot_id}' not found.")
        return 404  
