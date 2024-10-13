import unittest
import subprocess
import time
from client import InventoryClient

class TestEndToEnd(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server_a_process = subprocess.Popen(['python', 'server.py', '--port', '5001'])
        cls.server_b_process = subprocess.Popen(['python', 'server.py', '--port', '5002'])
        time.sleep(5)
        cls.client = InventoryClient("http://localhost:5001")

    @classmethod
    def tearDownClass(cls):
        cls.server_a_process.terminate()
        cls.server_b_process.terminate()
        cls.server_a_process.wait()
        cls.server_b_process.wait()
    def test_define_and_manage_inventory(self):
        response = self.client.define_stuff("widget", "A useful widget")
        self.assertEqual(response, {'message': "Defined type 'widget' with description 'A useful widget'."})

        response = self.client.add(10, "widget")
        self.assertEqual(response, {'message': "Added 10 of type 'widget'."})

        response = self.client.remove(5, "widget")
        self.assertEqual(response, {'message': "Removed 5 of type 'widget'."})

        response = self.client.get_count("widget")
        self.assertEqual(response, {'count': 5})

        response = self.client.undefine("widget")
        self.assertEqual(response, {'message': "Undefined type 'widget'."})

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
        self.assertEqual(count_response, {'count': -1})

    # New Tests
    #A4-e2e-1
    def test_define_stuff_routing(self):
        self.client.undefine("apple")
        response = self.client.define_stuff("apple", "A fruit")
        self.assertEqual(response, {'message': "Defined type 'apple' with description 'A fruit'."})

        self.client.undefine("zebra")
        response = self.client.define_stuff("zebra", "An animal")
        self.assertEqual(response, {'message': "Defined type 'zebra' with description 'An animal'."})
    #A4-e2e-2
    def test_add_routing(self):
        self.client.undefine("banana")
        self.client.undefine("mango")
        response = self.client.define_stuff("banana", "A yellow fruit")
        self.assertEqual(response, {'message': "Defined type 'banana' with description 'A yellow fruit'."})
        response = self.client.add(10, "banana")
        self.assertEqual(response, {'message': "Added 10 of type 'banana'."})
        response = self.client.define_stuff("mango", "A tropical fruit")
        self.assertEqual(response, {'message': "Defined type 'mango' with description 'A tropical fruit'."})
        response = self.client.add(5, "mango")
        self.assertEqual(response, {'message': "Added 5 of type 'mango'."})
    #A4-e2e-3
    def test_remove_routing(self):
        self.client.undefine("grape")
        self.client.undefine("nectarine")
        response = self.client.define_stuff("grape", "A small fruit")
        self.assertEqual(response, {'message': "Defined type 'grape' with description 'A small fruit'."})
        self.client.add(10, "grape")
        response = self.client.remove(3, "grape")
        self.assertEqual(response, {'message': "Removed 3 of type 'grape'."})
        response = self.client.define_stuff("nectarine", "A sweet fruit")
        self.assertEqual(response, {'message': "Defined type 'nectarine' with description 'A sweet fruit'."})
        self.client.add(7, "nectarine")
        response = self.client.remove(2, "nectarine")
        self.assertEqual(response, {'message': "Removed 2 of type 'nectarine'."})
    #A4-e2e-4
    def test_get_count_routing(self):
        self.client.undefine("lemon")
        self.client.undefine("orange")
        response = self.client.define_stuff("lemon", "A sour fruit")
        self.assertEqual(response, {'message': "Defined type 'lemon' with description 'A sour fruit'."})
        response = self.client.get_count("lemon")
        self.assertEqual(response, {'count': 0})

        response = self.client.define_stuff("orange", "A sweet fruit")
        self.assertEqual(response, {'message': "Defined type 'orange' with description 'A sweet fruit'."})
        response = self.client.get_count("orange")
        self.assertEqual(response, {'count': 0}) 

if __name__ == '__main__':
    unittest.main()
