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

    def test_define_and_manage_inventory(self):
        response = self.client.define_stuff("widget", "A useful widget")
        self.assertEqual(response, {'message': 'Defined type \'widget\' with description \'A useful widget\'.'})

        response = self.client.add(10, "widget")
        self.assertEqual(response, {'message': 'Added 10 of type \'widget\'.'})

        response = self.client.remove(5, "widget")
        self.assertEqual(response, {'message': 'Removed 5 of type \'widget\'.'})

        response = self.client.get_count("widget")
        self.assertEqual(response, {'count': 5})

        response = self.client.undefine("widget")
        self.assertEqual(response, {'message': 'Undefined type \'widget\'.'})

        response = self.client.get_count("widget")
        self.assertEqual(response, {'count': -1})

    def test_save_and_load_data(self):
        self.client.define_stuff("widget", "A useful widget")
        self.client.add(10, "widget")

        save_response = self.client.save_data()
        self.assertIn('snapshot_id', save_response)

        self.client.undefine("widget")

        load_response = self.client.load_data(save_response['snapshot_id'])
        self.assertEqual(load_response, {'message': 'Data loaded successfully.'})

        count_response = self.client.get_count("widget")
        self.assertEqual(count_response, {'count': 10})

    


if __name__ == '__main__':
    unittest.main()
