# test_client.py
import unittest
from unittest.mock import patch
from client import InventoryClient
import requests
import json

class TestInventoryClient(unittest.TestCase):

    @patch('requests.post')
    def test_define_stuff(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'message': 'Defined type \'widget\' with description \'A useful widget\'.'}
        
        client = InventoryClient("http://localhost:5000")
        response = client.define_stuff("widget", "A useful widget")
        
        self.assertEqual(response, {'message': 'Defined type \'widget\' with description \'A useful widget\'.'})
        mock_post.assert_called_once_with('http://localhost:5000/define_stuff', headers={'Content-Type': 'application/json'}, data=json.dumps({"type": "widget", "description": "A useful widget"}))

    @patch('requests.post')
    def test_add(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'message': 'Added 10 of type \'widget\'.'}
        
        client = InventoryClient("http://localhost:5000")
        response = client.add(10, "widget")
        
        self.assertEqual(response, {'message': 'Added 10 of type \'widget\'.'})
        mock_post.assert_called_once_with('http://localhost:5000/add', headers={'Content-Type': 'application/json'}, data=json.dumps({"quantity": 10, "type": "widget"}))

    @patch('requests.post')
    def test_remove(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'message': 'Removed 5 of type \'widget\'.'}
        
        client = InventoryClient("http://localhost:5000")
        response = client.remove(5, "widget")
        
        self.assertEqual(response, {'message': 'Removed 5 of type \'widget\'.'})
        mock_post.assert_called_once_with('http://localhost:5000/remove', headers={'Content-Type': 'application/json'}, data=json.dumps({"quantity": 5, "type": "widget"}))

    @patch('requests.post')
    def test_undefine(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'message': 'Undefined type \'widget\'.'}
        
        client = InventoryClient("http://localhost:5000")
        response = client.undefine("widget")
        
        self.assertEqual(response, {'message': 'Undefined type \'widget\'.'})
        mock_post.assert_called_once_with('http://localhost:5000/undefine', headers={'Content-Type': 'application/json'}, data=json.dumps({"type": "widget"}))

if __name__ == '__main__':
    unittest.main()

