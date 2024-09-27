import requests
import unittest
from unittest.mock import patch
from client import InventoryClient

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

    @patch('requests.get')
    def test_get_count(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'count': 10}
        
        client = InventoryClient("http://localhost:5000")
        response = client.get_count("widget")
        
        self.assertEqual(response, {'count': 10})
        mock_get.assert_called_once_with('http://localhost:5000/get_count', params={"type": "widget"})

    @patch('requests.get')
    def test_get_count_undefined(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'count': -1}
        
        client = InventoryClient("http://localhost:5000")
        response = client.get_count("undefined_item")
        
        self.assertEqual(response, {'count': -1})
        mock_get.assert_called_once_with('http://localhost:5000/get_count', params={"type": "undefined_item"})
    
    # adding the new unit tests
    @patch('requests.post')
    def test_save_data(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'id': 0}
        client = InventoryClient("http://localhost:5000")
        response = client.save_data()
        self.assertEqual(response, 0)
        mock_post.assert_called_once_with('http://localhost:5000/save_data', headers={'Content-Type': 'application/json'}, data=json.dumps({}))

    @patch('requests.post')
    def test_load_data(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'message': 'Success'}
        
        client = InventoryClient("http://localhost:5000")
        response = client.load_data(0)
        
        self.assertEqual(response, {'message': 'Success'})
        mock_post.assert_called_once_with('http://localhost:5000/load_data', headers={'Content-Type': 'application/json'}, data=json.dumps({"id": 0}))

    @patch('requests.post')
    def test_delete_data(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'message': 'Deleted Successfully'}
        
        client = InventoryClient("http://localhost:5000")
        response = client.delete_data(0)
        
        self.assertEqual(response, {'message': 'Deleted Successfully'})
        mock_post.assert_called_once_with('http://localhost:5000/delete_data', headers={'Content-Type': 'application/json'}, data=json.dumps({"id": 0}))


    @patch('requests.post')
    def test_cr_delete_data_failure(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'message': 'Failed'}
        
        client = InventoryClient("http://localhost:5000")
        response = client.delete_data('invalid-id')
        
        self.assertEqual(response, {'message': 'Failed'})
        mock_post.assert_called_once_with('http://localhost:5000/delete_data', headers={'Content-Type': 'application/json'}, data=json.dumps({"id": "invalid-id"}))

if __name__ == '__main__':
    unittest.main()
