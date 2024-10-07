import unittest
from unittest.mock import patch
from client import InventoryClient
import requests

class TestInventoryClient(unittest.TestCase):

    @patch('requests.post')
    def test_define_stuff(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'message': 'Defined type \'widget\' with description \'A useful widget\'.'
        }
        
        client = InventoryClient("http://localhost:5000")
        response = client.define_stuff("widget", "A useful widget")
        
        self.assertEqual(response, {'message': 'Defined type \'widget\' with description \'A useful widget\'.'})

    @patch('requests.post')
    def test_undefine(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'message': 'Undefined type \'widget\'.'
        }

        client = InventoryClient("http://localhost:5000")
        response = client.undefine("widget")

        self.assertEqual(response, {'message': 'Undefined type \'widget\'.'})

    @patch('requests.post')
    def test_add(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'message': 'Added 5 of type \'widget\'.'
        }
        
        client = InventoryClient("http://localhost:5000")
        response = client.add(5, "widget")
        
        self.assertEqual(response, {'message': 'Added 5 of type \'widget\'.'})

    @patch('requests.post')
    def test_remove(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'message': 'Removed 3 of type \'widget\'.'
        }
        
        client = InventoryClient("http://localhost:5000")
        response = client.remove(3, "widget")
        
        self.assertEqual(response, {'message': 'Removed 3 of type \'widget\'.'})

    @patch('requests.get')
    def test_get_count(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'count': 10}
        
        client = InventoryClient("http://localhost:5000")
        response = client.get_count("widget")
        
        self.assertEqual(response, {'count': 10})

    @patch('requests.post')
    def test_save_data(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'snapshot_id': '1'}
        
        client = InventoryClient("http://localhost:5000")
        response = client.save_data()
        
        self.assertEqual(response, {'snapshot_id': '1'})

    @patch('requests.post')
    def test_load_data(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'message': 'Data loaded successfully.'
        }
        
        client = InventoryClient("http://localhost:5000")
        response = client.load_data("1")
        
        self.assertEqual(response, {'message': 'Data loaded successfully.'})

    @patch('requests.post')
    def test_delete_data(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'message': 'Snapshot deleted successfully.'
        }
        
        client = InventoryClient("http://localhost:5000")
        response = client.delete_data("1")
        
        self.assertEqual(response, {'message': 'Snapshot deleted successfully.'})

if __name__ == '__main__':
    unittest.main()
