import unittest
import subprocess
import time
import requests
from client import InventoryClient

class TestEndToEnd(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server_process = subprocess.Popen(['python', 'server.py'])
        time.sleep(5)
        cls.client = InventoryClient("http://localhost:5000")

    @classmethod
    def tearDownClass(cls):
        cls.server_process.terminate()
        cls.server_process.wait()

    def setUp(self):
        try:
            self.client.undefine("widget")
        except Exception:
            pass

    def test_define_and_manage_inventory(self):
        response = self.client.define_stuff("widget", "A useful widget")
        self.assertEqual(response, {'message': 'Defined type \'widget\' with description \'A useful widget\'.'})

        # Add items
        response = self.client.add(10, "widget")
        self.assertEqual(response, {'message': 'Added 10 of type \'widget\'.'})

        # Remove items
        response = self.client.remove(5, "widget")
        self.assertEqual(response, {'message': 'Removed 5 of type \'widget\'.'})

        # Check item count
        response = self.client.get_count("widget")
        self.assertEqual(response, {'count': 5})

        # Undefine the item
        response = self.client.undefine("widget")
        self.assertEqual(response, {'message': 'Undefined type \'widget\'.'})

        # Check item count for undefined item
        response = self.client.get_count("widget")
        self.assertEqual(response, {'count': -1})
        
        # Added new end to end test cases
        
    def test_backup_functionality(self):
        self.client.define_stuff("widget", "A useful widget")
        self.client.add(10, "widget")
        snapshot_id = self.client.save_data()
        self.assertIsNotNone(snapshot_id)
        self.client.undefine("widget")
        load_result = self.client.load_data(snapshot_id)
        self.assertEqual(load_result, {'message': 'Success'})
        response = self.client.get_count("widget")
        self.assertEqual(response, {'count': 10})
        delete_result = self.client.delete_data(snapshot_id)
        self.assertEqual(delete_result, {'message': 'Deleted Successfully'})


    def test_cr_save_load_delete_inventory(self):
        response = self.client.define_stuff("test", "A useful test")
        self.assertEqual(response, {'message': 'Defined type \'test\' with description \'A useful test\'.'})

        response = self.client.add(10, "test")
        self.assertEqual(response, {'message': 'Added 10 of type \'test\'.'})

        snapshot_id = self.client.save_data()
        self.assertIsNotNone(snapshot_id)

        response = self.client.remove(10, "test")
        self.assertEqual(response, {'message': 'Removed 10 of type \'test\'.'})
        response = self.client.undefine("test")
        self.assertEqual(response, {'message': 'Undefined type \'test\'.'})

        load_response = self.client.load_data(snapshot_id)
        self.assertEqual(load_response, {'message': 'Success'})

        response = self.client.get_count("test")
        self.assertEqual(response, {'count': 10})

        delete_response = self.client.delete_data(snapshot_id)
        self.assertEqual(delete_response, {'message': 'Deleted Successfully'})

        load_response_after_delete = self.client.load_data(snapshot_id)
        self.assertEqual(load_response_after_delete, {'message': 'Failed'})

        self.client.undefine("test")

if __name__ == '__main__':
    unittest.main()
